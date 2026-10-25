"""LiveKit voice agent for trip planning.

Real APIs: weather (Open-Meteo), places/restaurants/hotels (Geoapify), flights
(RapidAPI flights-sky, Booking.com-backed). Booking itself is simulated — no real
payment or reservation ever occurs.

Unlike the from-scratch version in scratch_ai_voice_agent/, LiveKit's AgentSession
handles the STT->LLM->TTS pipeline, turn detection, and conversation history itself —
so the custom reliability engineering built there (forced tool_choice, retry-with-
backoff, context compaction) isn't reproduced here; LiveKit's own session management
covers most of what that was compensating for. State is just plain attributes on the
Agent instance, mutated directly by whichever function_tool the model calls — no
generic "update_trip_state" tool needed, since each tool's arguments are already typed
and validated by LiveKit itself.
"""

import asyncio
import csv
import logging
import os
import secrets
from datetime import datetime, timezone
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RunContext,
    cli,
    function_tool,
)
from livekit.agents import llm
from livekit.agents.llm import FallbackAdapter
from livekit.agents.metrics import EOUMetrics, LLMMetrics, STTMetrics, TTSMetrics
from livekit.plugins import cartesia, groq, silero

from src.state import TripState
from src.weather_client import WeatherClient
from src.geoapify_client import GeoapifyClient
from src.flight_client import FlightClient

load_dotenv(override=True)  # project .env always wins over stale ambient env vars
logger = logging.getLogger("trip-agent")

# Clean terminal by default: LiveKit's internal DEBUG/INFO logs (VAD ticks, tool
# execution traces, raw event dumps) are useful for deep debugging but drown out the
# actual conversation. Override with --log-level debug on the command line if you
# need the full firehose back.
logging.getLogger("livekit").setLevel(logging.WARNING)

SYSTEM_PROMPT = """You are a trip planning voice assistant. Today's date is {today}. When the user gives
a date without a year (e.g. "October 1st to 3rd"), assume the NEAREST upcoming occurrence of that date
relative to today — never default to a past year. Guide the user through these stages, in order:

1. Collect preferences: destination region, budget, travel dates, number of travelers, interests.
   Ask ONE question at a time — never a list of several. Wait for each answer before asking the next.
2. Suggest 2-3 candidate destinations that fit their preferences, with a short reason for each.
3. Once a destination is chosen, call set_destination, then build a day-by-day itinerary and save it
   with set_itinerary. For globally famous landmarks, use your own knowledge. Call find_restaurants
   for the destination and weave a couple of REAL restaurant names into the itinerary — never invent
   restaurant names.
4. Once destination and specific dates are known, call get_weather_forecast to check real conditions.
   If it fails (dates too far out — only ~16 days ahead are covered), say so plainly and fall back to
   general seasonal expectations instead of inventing numbers.
5. Once the user gives an origin city/airport and a specific date, call set_origin, then call
   search_flights (real prices). Present the top few real options and ask which they want. Once
   chosen, save it with set_chosen_flight. NEVER state a specific flight price/time/airline unless
   search_flights actually returned it earlier in this conversation.
6. Call find_hotels for the destination and pick one or two REAL hotels by name from the results, with
   an ESTIMATED nightly price (no real pricing API exists — but the hotel name/area must be real).
   Save the choice with set_hotel_choice, clearly labeling the price as an estimate.
7. Once destination, itinerary, chosen flight, and chosen hotel are all set, and the user explicitly
   confirms ("book it" / "let's book" / similar), call book_trip. Present the result as a SIMULATED
   confirmation — make clear no real payment or booking happened.

This is a spoken, voice-only conversation: keep replies short and natural, like real speech, not a
written report. Summarizing briefly is fine, but never skip a stage just to keep it short — still do
the actual work (real searches, real persistence), just describe it concisely out loud.
"""


# Tool results that return large lists (real API data) rather than short confirmations.
# Once a turn has passed, the assistant already used the fresh data to speak its reply —
# so the raw JSON just sits in history being resent every subsequent call for no benefit.
# Measured directly: per-call token cost climbed from ~2100 to ~3900 tokens across one
# conversation as these piled up, which is what drove both Groq keys into their 8000 TPM
# limit at nearly the same time.
COMPACTABLE_TOOLS = {"find_hotels", "find_restaurants", "search_flights", "get_weather_forecast"}
COMPACTED_PLACEHOLDER = "[older result already used and spoken to the user — call the tool again if you need fresh data]"


class TripAgent(Agent):
    def __init__(self):
        today = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
        super().__init__(instructions=SYSTEM_PROMPT.format(today=today))
        self.state = TripState()
        self.weather = WeatherClient()
        self.geoapify = GeoapifyClient()
        self.flights = FlightClient()

    async def on_enter(self):
        self.session.generate_reply()

    async def on_user_turn_completed(self, turn_ctx: llm.ChatContext, new_message: llm.ChatMessage) -> None:
        changed = False
        for item in turn_ctx.items:
            if (
                item.type == "function_call_output"
                and item.name in COMPACTABLE_TOOLS
                and item.output != COMPACTED_PLACEHOLDER
            ):
                item.output = COMPACTED_PLACEHOLDER
                changed = True
        if changed:
            await self.update_chat_ctx(turn_ctx.copy())

    @function_tool
    async def update_preferences(
        self,
        context: RunContext,
        region: str = "",
        budget: str = "",
        dates: str = "",
        travelers: str = "",
        interests: str = "",
    ) -> str:
        """Persist any trip preferences given so far. Call as soon as any are known —
        leave the rest blank; this can be called multiple times as more comes up.

        Args:
            region: Destination region or country, if known.
            budget: Budget for the trip, if known.
            dates: Travel dates, if known.
            travelers: Number of travelers, if known.
            interests: Interests (e.g. mountains, food), if known.
        """
        updates = {
            k: v
            for k, v in {
                "region": region,
                "budget": budget,
                "dates": dates,
                "travelers": travelers,
                "interests": interests,
            }.items()
            if v
        }
        self.state.preferences.update(updates)
        return "Preferences recorded."

    @function_tool
    async def set_destination(self, context: RunContext, destination: str) -> str:
        """Record the destination once the user has chosen one.

        Args:
            destination: The chosen destination city.
        """
        self.state.destination = destination
        return f"Destination set to {destination}."

    @function_tool
    async def set_origin(self, context: RunContext, origin: str) -> str:
        """Record the user's departure city/airport once given.

        Args:
            origin: The departure city or airport.
        """
        self.state.origin = origin
        return f"Origin set to {origin}."

    @function_tool
    async def set_itinerary(self, context: RunContext, itinerary: str) -> str:
        """Save the day-by-day itinerary once drafted.

        Args:
            itinerary: The full day-by-day itinerary text.
        """
        self.state.itinerary = itinerary
        return "Itinerary saved."

    @function_tool
    async def get_weather_forecast(self, context: RunContext, city: str, start_date: str, end_date: str):
        """Get a REAL weather forecast for a city over a date range (free API, no key
        needed). Only covers roughly the next 16 days from today.

        Args:
            city: City name.
            start_date: Start date, YYYY-MM-DD.
            end_date: End date, YYYY-MM-DD.
        """
        try:
            # to_thread: get_forecast() uses blocking requests.get() — running it
            # directly would stall the whole agent loop (audio, turn detection, every
            # other in-flight task) for the full HTTP round-trip, which LiveKit itself
            # flags as a real problem, unlike the scratch version's single-threaded loop.
            forecast = await asyncio.to_thread(self.weather.get_forecast, city, start_date, end_date)
        except Exception as exc:
            return f"Weather forecast unavailable: {exc}"
        self.state.weather = forecast
        return forecast

    @function_tool
    async def find_restaurants(self, context: RunContext, city: str):
        """Find REAL nearby restaurants for a city (free API).

        Args:
            city: City name.
        """
        try:
            places = await asyncio.to_thread(self.geoapify.find_places, city, "catering.restaurant")
        except Exception as exc:
            return f"Restaurant search failed: {exc}"
        self.state.restaurants = places
        return places

    @function_tool
    async def find_hotels(self, context: RunContext, city: str):
        """Find REAL nearby hotels for a city (free API) — no pricing included, give
        your own nightly-price estimate for whichever one you recommend.

        Args:
            city: City name.
        """
        try:
            places = await asyncio.to_thread(self.geoapify.find_places, city, "accommodation.hotel")
        except Exception as exc:
            return f"Hotel search failed: {exc}"
        self.state.hotel_options = places
        return places

    @function_tool
    async def search_flights(
        self, context: RunContext, origin: str, destination: str, depart_date: str, adults: int = 1
    ):
        """Search REAL one-way flight prices (free API).

        Args:
            origin: Origin IATA airport code, e.g. 'JFK'.
            destination: Destination IATA airport code, e.g. 'ISB'.
            depart_date: Departure date, YYYY-MM-DD.
            adults: Number of travelers.
        """
        try:
            offers = await asyncio.to_thread(self.flights.search_one_way, origin, destination, depart_date, adults)
        except Exception as exc:
            return f"Flight search failed: {exc}"
        self.state.flight_options = offers
        return offers

    @function_tool
    async def set_chosen_flight(self, context: RunContext, summary: str) -> str:
        """Record which real flight option the user picked.

        Args:
            summary: Short summary of the chosen flight (airline, price, time).
        """
        self.state.flights = summary
        return "Flight choice saved."

    @function_tool
    async def set_hotel_choice(self, context: RunContext, summary: str) -> str:
        """Record the chosen hotel and its estimated nightly price.

        Args:
            summary: Hotel name/area and estimated nightly price.
        """
        self.state.hotel = summary
        return "Hotel choice saved."

    @function_tool
    async def book_trip(self, context: RunContext):
        """Simulate finalizing the booking. Only call once destination, itinerary,
        chosen flight, and chosen hotel are all set, and the user has explicitly
        confirmed. No real payment or booking ever occurs."""
        s = self.state
        missing = [
            f
            for f, v in [
                ("destination", s.destination),
                ("itinerary", s.itinerary),
                ("flights", s.flights),
                ("hotel", s.hotel),
            ]
            if not v
        ]
        if missing:
            return f"Cannot book yet — still missing: {', '.join(missing)}."

        confirmation = {
            "simulated": True,
            "confirmation_code": "TRIP-" + secrets.token_hex(3).upper(),
            "destination": s.destination,
            "booked_at": datetime.now(timezone.utc).isoformat(),
            "note": "No real payment or booking occurred. This is a demo confirmation only.",
        }
        self.state.booking_confirmation = confirmation
        return confirmation


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


LOG_PATH = "conversation_log.csv"
LOG_FIELDS = ["timestamp", "type", "duration", "detail"]


def _log_metric(row: dict):
    """Same-shaped CSV logging as the scratch version, but using LiveKit's own
    metrics (real STT/LLM/TTS timing it measures internally) instead of our own
    wall-clock timers — lets us directly compare the two implementations on equal
    footing rather than guessing whether LiveKit actually fixed the slowness."""
    is_new = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def _on_metrics_collected(ev: MetricsCollectedEvent):
    """Logged to CSV only, not printed — keeps the terminal to just the conversation.
    Open conversation_log.csv afterward for the timing breakdown. Skips high-frequency
    types we don't otherwise analyze (vad_metrics fires ~2x/second, pure noise here)."""
    m = ev.metrics
    row = {"timestamp": datetime.now().isoformat(timespec="seconds"), "type": m.type}
    if isinstance(m, STTMetrics):
        row["duration"] = round(m.duration, 2)
        row["detail"] = f"audio_duration={m.audio_duration:.2f}s (pure transcription time, not how long you talked)"
    elif isinstance(m, LLMMetrics):
        row["duration"] = round(m.duration, 2)
        row["detail"] = f"ttft={m.ttft:.2f}s, tokens/s={m.tokens_per_second:.1f}, total_tokens={m.total_tokens}"
    elif isinstance(m, TTSMetrics):
        row["duration"] = round(m.duration, 2)
        row["detail"] = f"ttfb={m.ttfb:.2f}s (time to first audio byte)"
    elif isinstance(m, EOUMetrics):
        row["duration"] = round(m.end_of_utterance_delay, 2)
        row["detail"] = (
            f"end_of_utterance_delay={m.end_of_utterance_delay:.2f}s "
            f"(if too short, risks cutting off your last word), "
            f"transcription_delay={m.transcription_delay:.2f}s"
        )
    else:
        return  # vad_metrics, eot_inference_metrics, interruption_metrics — too noisy, skip
    _log_metric(row)


server = AgentServer()
server.setup_fnc = prewarm


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    # Four Groq API keys from separate accounts, each with its own independent 8000
    # TPM quota (confirmed empirically: burning one key's quota down did not move
    # the other's). FallbackAdapter tries them in order, and on a failure (e.g. the
    # 429 rate-limit error a maxed-out key throws) immediately retries the same
    # request on the next one — mid-conversation, without restarting the session.
    # Four keys instead of two means a user is far less likely to notice any delay
    # before one of them has spare quota.
    groq_llms = [
        groq.LLM(model="openai/gpt-oss-120b", api_key=os.environ[f"GROQ_API_KEY_{i}"])
        for i in range(1, 5)
    ]

    session = AgentSession(
        stt=groq.STT(model="whisper-large-v3-turbo", api_key=os.environ["GROQ_API_KEY_1"]),
        llm=FallbackAdapter(groq_llms),
        tts=cartesia.TTS(model="sonic-3.6", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=ctx.proc.userdata["vad"],
        # Preemptive generation defaults to up to 3 extra speculative LLM calls per user
        # turn (LiveKit's own default, see voice/turn.py). On an 8000 TPM free-tier budget,
        # that multiplies call volume 3-4x per turn and burns quota through sheer call
        # count rather than call size — confirmed directly in conversation_log.csv (three
        # llm_metrics rows within the same second). Disabled since we're quota-constrained.
        turn_handling={"preemptive_generation": {"enabled": False}},
    )
    session.on("metrics_collected", _on_metrics_collected)

    await session.start(agent=TripAgent(), room=ctx.room)
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
