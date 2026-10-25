"""Client for Geoapify's Places and Routing APIs.

Free tier: 3,000 requests/day, no credit card required. Requires an API key
(GEOAPIFY_API_KEY) — city names are resolved to coordinates via the shared
keyless geocoder rather than spending Geoapify credits on that step.
"""

import os
import requests
from src.geocode import geocode

BASE_URL = "https://api.geoapify.com"
REQUEST_TIMEOUT = 15  # seconds — a hung upstream must never block the agent forever


class GeoapifyClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GEOAPIFY_API_KEY")

    def find_places(
        self,
        city: str,
        category: str,
        radius_m: int = 6000,
        limit: int = 10,
    ) -> list[dict]:
        """category examples: 'tourism.sights', 'catering.restaurant', 'catering.cafe',
        'tourism.attraction', 'entertainment'. See Geoapify's Places category list for more."""
        loc = geocode(city)
        resp = requests.get(
            f"{BASE_URL}/v2/places",
            params={
                "categories": category,
                "filter": f"circle:{loc['longitude']},{loc['latitude']},{radius_m}",
                "bias": f"proximity:{loc['longitude']},{loc['latitude']}",
                "limit": limit,
                "lang": "en",
                "apiKey": self.api_key,
            },
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        places = []
        for feature in resp.json().get("features", []):
            props = feature.get("properties", {})
            if not props.get("name"):
                continue
            places.append(
                {
                    "name": props.get("name"),
                    "address": props.get("formatted"),
                    "lat": props.get("lat"),
                    "lon": props.get("lon"),
                }
            )
        return places

    def get_route(self, waypoints: list[str], mode: str = "walk") -> dict:
        """Each waypoint is either 'lat,lon' or a place name to resolve via geocoding.
        mode: 'walk', 'drive', 'bicycle', or 'transit' (where supported)."""
        resolved = []
        for wp in waypoints:
            parts = wp.split(",")
            if len(parts) == 2 and all(_is_float(p) for p in parts):
                resolved.append(wp.strip())
            else:
                loc = geocode(wp)
                resolved.append(f"{loc['latitude']},{loc['longitude']}")

        resp = requests.get(
            f"{BASE_URL}/v1/routing",
            params={
                "waypoints": "|".join(resolved),
                "mode": mode,
                "apiKey": self.api_key,
            },
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        feature = resp.json().get("features", [{}])[0]
        props = feature.get("properties", {})
        distance_m = props.get("distance", 0)
        time_s = props.get("time", 0)
        return {
            "distance_km": round(distance_m / 1000, 2),
            "time_min": round(time_s / 60, 1),
            "mode": mode,
        }


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
