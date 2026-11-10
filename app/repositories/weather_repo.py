"""Data access шар."""
from datetime import date, datetime, timedelta
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.orm import Weather, Wind

class WeatherRepository:
    def __init__(self, session: Session): self.session = session

    def find(self, country: str, day: date, location: str | None = None):
        start = datetime.combine(day, datetime.min.time())
        q = (select(Weather, Wind).join(Wind, Wind.weather_id == Weather.id)
             .where(func.lower(Weather.country) == country.lower(),
                    Weather.last_updated >= start, Weather.last_updated < start + timedelta(days=1)))
        if location:
            q = q.where(func.lower(Weather.location_name) == location.lower())
        return self.session.execute(q.order_by(Weather.location_name)).all()
