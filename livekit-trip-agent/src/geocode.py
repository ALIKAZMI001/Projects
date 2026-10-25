"""Shared city-name -> coordinates lookup, free and keyless (Open-Meteo geocoding).

Used by both weather_client.py and geoapify_client.py so neither has to duplicate
this or spend Geoapify's metered credits just to resolve a city name.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
REQUEST_TIMEOUT = 15  # seconds — a hung upstream must never block the agent forever


def geocode(city: str) -> dict:
    resp = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        raise ValueError(f"Could not find location: {city}")
    loc = results[0]
    return {
        "name": loc["name"],
        "country": loc.get("country", ""),
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
    }
