"""Client for Open-Meteo — free, public weather API, no API key or signup required.

Note: the forecast endpoint only has real data roughly 16 days out. For dates further
in the future (the common case for trip planning), the API returns an error, which
callers should surface honestly rather than inventing a forecast.
"""

import requests
from src.geocode import geocode

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 15  # seconds — a hung upstream must never block the agent forever


class WeatherClient:
    def get_forecast(self, city: str, start_date: str, end_date: str) -> dict:
        loc = geocode(city)

        forecast_resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto",
                "start_date": start_date,
                "end_date": end_date,
            },
            timeout=REQUEST_TIMEOUT,
        )
        forecast_resp.raise_for_status()
        daily = forecast_resp.json().get("daily", {})

        days = []
        for i, date in enumerate(daily.get("time", [])):
            days.append(
                {
                    "date": date,
                    "high_c": daily["temperature_2m_max"][i],
                    "low_c": daily["temperature_2m_min"][i],
                    "precipitation_mm": daily["precipitation_sum"][i],
                }
            )
        return {"location": f"{loc['name']}, {loc['country']}", "days": days}
