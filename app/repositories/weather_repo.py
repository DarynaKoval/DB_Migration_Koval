"""ШАР ДОСТУПУ ДО ДАНИХ: запити до бази для пошуку погоди."""
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.orm import Weather


class WeatherRepository:

    def __init__(self, session: Session):
        self.session = session

    def find(self, country, day, location=None):
        """Уся погода по країні за один день (можна ще уточнити місто)."""
        start = datetime.combine(day, datetime.min.time())   # 00:00 цього дня
        end = start + timedelta(days=1)                       # 00:00 наступного дня
        query = (
            self.session.query(Weather)
            .options(joinedload(Weather.astronomy))           # одразу з таблицею astronomy
            .filter(func.lower(Weather.country) == country.lower())
            .filter(Weather.last_updated >= start, Weather.last_updated < end)
        )
        if location:
            query = query.filter(func.lower(Weather.location_name) == location.lower())
        return query.order_by(Weather.last_updated).all()

    def date_range(self, country):
        """Перша й остання дата, за які є дані по країні."""
        return (
            self.session.query(func.min(Weather.last_updated), func.max(Weather.last_updated))
            .filter(func.lower(Weather.country) == country.lower())
            .one()
        )
