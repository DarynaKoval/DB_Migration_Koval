"""Бізнес-логіка."""
from datetime import date
from app.repositories.weather_repo import WeatherRepository

MAX_WIND_KPH = 36  # 10 м/с

def should_go_outside(wind_kph: float | None) -> bool:
    """Формула 'чи варто виходити': вітер не сильніший за 10 м/с. Та сама логіка в міграції 003."""
    return wind_kph is not None and wind_kph <= MAX_WIND_KPH

class WeatherService:
    def __init__(self, repo: WeatherRepository): self.repo = repo

    def report(self, country: str, day: date, location: str | None = None) -> list[dict]:
        return [{"location": w.location_name, "time": w.last_updated.isoformat(sep=" "),
                 "sunrise": str(w.sunrise), "wind_kph": x.wind_kph, "wind_mph": x.wind_mph,
                 "wind_degree": x.wind_degree, "wind_direction": x.wind_direction.value if x.wind_direction else None,
                 "gust_kph": x.gust_kph, "go_outside": "так" if x.go_outside else "ні"}
                for w, x in self.repo.find(country, day, location)]
