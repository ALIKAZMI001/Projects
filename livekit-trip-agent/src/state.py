"""Holds the trip planning state across a conversation."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TripState:
    preferences: dict = field(default_factory=dict)
    destination: Optional[str] = None
    origin: Optional[str] = None
    itinerary: Optional[str] = None
    flights: Optional[str] = None
    hotel: Optional[str] = None
    weather: Optional[dict] = None
    restaurants: Optional[list] = None
    hotel_options: Optional[list] = None
    flight_options: Optional[list] = None
    booking_confirmation: Optional[dict] = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not value or not hasattr(self, key):
                continue
            if key == "preferences" and isinstance(value, dict):
                self.preferences.update(value)
            else:
                setattr(self, key, value)

    def summary(self) -> str:
        parts = []
        if self.preferences:
            parts.append(f"Preferences: {self.preferences}")
        if self.destination:
            parts.append(f"Destination: {self.destination}")
        if self.itinerary:
            parts.append("Itinerary: set")
        if self.weather:
            parts.append(f"Weather: {self.weather}")
        if self.restaurants:
            parts.append(f"Restaurants: {len(self.restaurants)} found")
        if self.hotel_options:
            parts.append(f"Hotel options: {len(self.hotel_options)} found")
        if self.flight_options:
            parts.append(f"Flight options: {len(self.flight_options)} found")
        if self.flights:
            parts.append(f"Flights: {self.flights}")
        if self.hotel:
            parts.append(f"Hotel: {self.hotel}")
        if self.booking_confirmation:
            parts.append(f"Booking: {self.booking_confirmation}")
        return "\n".join(parts) if parts else "No trip details captured yet."
