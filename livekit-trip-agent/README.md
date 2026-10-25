# LiveKit Trip Agent

A real-time **voice** travel planner. You talk to it; it collects your preferences,
suggests destinations, builds a day-by-day itinerary, checks live weather, finds real
restaurants, hotels and flight prices, and finally produces a *simulated* booking
confirmation.

> Booking is deliberately simulated — no payment, no reservation, no external write
> ever happens.

## What it does

| Stage | Tool | Data source |
| --- | --- | --- |
| Collect preferences | `update_preferences` | conversation |
| Pick a destination | `set_destination` | conversation |
| Build the itinerary | `set_itinerary`, `find_restaurants` | LLM knowledge + Geoapify |
| Check the forecast | `get_weather_forecast` | Open-Meteo (keyless) |
| Search flights | `search_flights` | RapidAPI flights-sky (Booking.com backend) |
| Choose a hotel | `find_hotels`, `set_hotel_choice` | Geoapify |
| Confirm | `book_trip` | simulated |

## Architecture

```
browser / phone (netlify_deploy/index.html)
        │  WebRTC
        ▼
   LiveKit room  ◄──►  AgentSession  ──►  STT   (Groq whisper-large-v3-turbo)
                            │              LLM   (Groq gpt-oss-120b, 4-key fallback)
                            │              TTS   (Cartesia sonic-3.6)
                            │              VAD   (Silero)
                            ▼
                    TripAgent (function tools)  ──►  weather / places / flights APIs
```

## Engineering notes

These are the parts that took real iteration:

- **Four-key LLM fallback.** Each Groq key has an independent free-tier quota.
  `FallbackAdapter` tries them in order and retries mid-conversation on a 429, so
  hitting a rate limit doesn't end the call.
- **Context compaction.** Tool results from `find_hotels`, `find_restaurants`,
  `search_flights` and `get_weather_forecast` are large JSON blobs. Once a turn has
  used them, `on_user_turn_completed` replaces them with a short placeholder. Token
  cost per call was measured climbing ~2 100 → ~3 900 across one conversation before
  this; that growth is what exhausted the quotas.
- **Preemptive generation disabled.** LiveKit's default can fire up to three
  speculative LLM calls per user turn, which triples quota burn on a free tier. It is
  turned off explicitly.
- **Blocking I/O pushed off the event loop.** Every HTTP client call is wrapped in
  `asyncio.to_thread`; a slow upstream would otherwise stall audio and turn
  detection.
- **Honest failure.** If the forecast window is too far out (~16 days max), the agent
  says so and falls back to seasonal expectations rather than inventing numbers.
- **Metrics to CSV.** STT/LLM/TTS/end-of-utterance timings are logged to
  `conversation_log.csv` via `MetricsCollectedEvent`, keeping the terminal to just
  the conversation.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the keys:

```bash
cp .env.example .env
```

```bash
python agent.py console         # talk in the terminal, no LiveKit room needed
python agent.py dev             # connect to your LiveKit project
```

The web console in `netlify_deploy/` is a single static page — deploy it to Netlify
and point it at your LiveKit URL and token endpoint.

## Environment variables

| Variable | Used for |
| --- | --- |
| `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` | LiveKit project credentials |
| `GROQ_API_KEY_1` … `GROQ_API_KEY_4` | STT + LLM quota pool |
| `CARTESIA_API_KEY` | Text-to-speech |
| `GEOAPIFY_API_KEY` | Restaurants and hotels |
| `RAPIDAPI_KEY`, `RAPIDAPI_KEY_2`, `RAPIDAPI_FLIGHTS_HOST` | Flight search |

## Deployment

`Dockerfile` builds a slim, non-root Python 3.13 image with dependencies installed in
a venv and model files pre-downloaded at build time (so code-only changes hit the
layer cache). `livekit.toml` holds the project/agent IDs.

## Stack

`livekit-agents` · `livekit-plugins-groq` · `livekit-plugins-cartesia` ·
`livekit-plugins-silero` · `requests` · `python-dotenv`
