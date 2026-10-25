"""Client for the 'flights-sky' API on RapidAPI — Booking.com-backed flight search.

This same RapidAPI listing exposes three backends. The Skyscanner-backed one
(/web/flights/...) is broken server-side (reproducible 431 errors). The Google
Flights one (/google/flights/...) works but is slow — 20-45s, since it's a live
scrape. This Booking.com-backed one (/bookingcom/...) is both real and MUCH
faster (~10s observed) because Booking.com serves it from cache rather than
scraping live each time (its response includes "source": "cache").

IATA airport codes just need a ".AIRPORT" suffix for this endpoint's departId/
arrivalId — no separate ID-resolution step needed, unlike the Skyscanner path.

Multiple API keys supported with automatic fallback on rate limit (429) or auth errors.
"""

import os
import requests

BASE_URL = "https://flights-sky.p.rapidapi.com"
REQUEST_TIMEOUT = 25  # seconds — generous margin over the ~10s observed in practice


def _load_api_keys() -> list[str]:
    """Load all RapidAPI keys from environment (RAPIDAPI_KEY, RAPIDAPI_KEY_2, RAPIDAPI_KEY_3...)."""
    keys = []
    primary = os.environ.get("RAPIDAPI_KEY")
    if primary:
        keys.append(primary)
    i = 2
    while True:
        key = os.environ.get(f"RAPIDAPI_KEY_{i}")
        if not key:
            break
        keys.append(key)
        i += 1
    return keys


class FlightClient:
    def __init__(self, api_keys: list[str] | None = None, host: str | None = None):
        self.api_keys = api_keys or _load_api_keys()
        if not self.api_keys:
            raise ValueError("No RapidAPI keys found. Set RAPIDAPI_KEY (and optionally RAPIDAPI_KEY_2, RAPIDAPI_KEY_3...) in environment.")
        self.host = host or os.environ.get("RAPIDAPI_FLIGHTS_HOST", "flights-sky.p.rapidapi.com")
        self._key_index = 0

    def _headers(self, key: str) -> dict:
        return {"X-RapidAPI-Key": key, "X-RapidAPI-Host": self.host}

    def _try_request(self, key: str, params: dict) -> requests.Response:
        return requests.get(
            f"{BASE_URL}/bookingcom/search-oneway",
            headers=self._headers(key),
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

    def search_one_way(
        self,
        origin: str,
        destination: str,
        depart_date: str,
        adults: int = 1,
        max_results: int = 5,
    ) -> list[dict]:
        """origin/destination are IATA airport codes (e.g. 'JFK'), depart_date is YYYY-MM-DD.
        Tries each API key in order until one succeeds or all are exhausted.
        """
        params = {
            "departId": f"{origin}.AIRPORT",
            "arrivalId": f"{destination}.AIRPORT",
            "departDate": depart_date,
            "adults": adults,
        }

        last_error = None
        for key in self.api_keys:
            try:
                resp = self._try_request(key, params)
                if resp.status_code == 429 or resp.status_code == 401 or resp.status_code == 403:
                    last_error = f"Key rejected (HTTP {resp.status_code})"
                    continue
                resp.raise_for_status()
                data = resp.json().get("data", {})

                offers = []
                for offer in data.get("flightOffers", [])[:max_results]:
                    segment = offer.get("segments", [{}])[0]
                    legs = segment.get("legs", [])
                    first_leg = legs[0] if legs else {}
                    carriers = first_leg.get("carriersData") or [{}]

                    price = offer.get("priceBreakdown", {}).get("total", {})
                    price_usd = round(price.get("units", 0) + price.get("nanos", 0) / 1e9, 2)

                    offers.append(
                        {
                            "price_usd": price_usd,
                            "airline": carriers[0].get("name"),
                            "stops": max(len(legs) - 1, 0),
                            "duration_min": round(segment.get("totalTime", 0) / 60),
                            "departure": f"{segment.get('departureAirport', {}).get('code')} {segment.get('departureTime')}",
                            "arrival": f"{segment.get('arrivalAirport', {}).get('code')} {segment.get('arrivalTime')}",
                        }
                    )
                return offers
            except requests.RequestException as e:
                last_error = str(e)
                continue

        raise RuntimeError(f"All RapidAPI keys exhausted. Last error: {last_error}")
