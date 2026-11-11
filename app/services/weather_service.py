"""ШАР БІЗНЕС-ЛОГІКИ: пошук погоди з перевіркою введених даних."""
from datetime import datetime

from app.repositories.weather_repo import WeatherRepository


class SearchError(Exception):
    """Помилка, яку треба просто показати користувачу."""


class WeatherService:

    def __init__(self, repo: WeatherRepository):
        self.repo = repo

    def search(self, country, date_text, location=None):
        try:
            day = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            raise SearchError("Дату треба писати у форматі РРРР-ММ-ДД, наприклад 2024-05-16")

        records = self.repo.find(country, day, location)
        if not records:
            first, last = self.repo.date_range(country)
            if first is None:
                raise SearchError(f"Країни '{country}' в базі немає. Перевір назву (англійською).")
            where = f"{country}, {location}" if location else country
            raise SearchError(f"Для {where} за {date_text} даних немає. "
                              f"По країні {country} дані є з {first:%Y-%m-%d} по {last:%Y-%m-%d}.")
        return records
