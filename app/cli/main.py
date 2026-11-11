"""ШАР ПРЕДСТАВЛЕННЯ (консоль).

Приклад:  python -m app.cli.main Ukraine 2024-05-16
          python -m app.cli.main Ukraine 2024-05-16 --location Kyiv
"""
import argparse

from sqlalchemy.orm import Session

from app.config import DATABASE_URL
from app.db import create_db_engine
from app.repositories.weather_repo import WeatherRepository
from app.services.weather_service import SearchError, WeatherService


def fmt_time(t):
    return t.strftime("%H:%M") if t else "немає"


def show(value, unit=""):
    return f"{value}{unit}" if value is not None else "немає"


def print_weather(w):
    a = w.astronomy
    print()
    print("=" * 50)
    print(f"{w.location_name}, {w.country} | {w.last_updated:%Y-%m-%d %H:%M}")
    print("=" * 50)
    print(f"Погода:   {w.condition_text}, {show(w.temperature_celsius, ' °C')}")
    print(f"Вітер:    {show(w.wind_kph, ' км/год')}, {show(w.wind_degree, '°')}, "
          f"напрям {show(w.wind_direction)}")
    print(f"Сонце:    схід {fmt_time(a.sunrise)}, захід {fmt_time(a.sunset)}")
    print(f"Місяць:   схід {fmt_time(a.moonrise)}, захід {fmt_time(a.moonset)}")
    print(f"          фаза {show(a.moon_phase)}, освітленість {show(a.moon_illumination, ' %')}")
    print(f"Чи варто виходити на вулицю: {'ТАК' if a.go_outside else 'НІ'}")


def main():
    p = argparse.ArgumentParser(description="Пошук погоди за країною і датою")
    p.add_argument("country", help="країна англійською, напр. Ukraine")
    p.add_argument("date", help="дата у форматі РРРР-ММ-ДД")
    p.add_argument("--location", help="місто (необов'язково)")
    a = p.parse_args()

    print("База даних:", DATABASE_URL.split(":")[0])
    with Session(create_db_engine(DATABASE_URL)) as session:
        service = WeatherService(WeatherRepository(session))
        try:
            records = service.search(a.country, a.date, a.location)
        except SearchError as e:
            print(e)
            return
        print(f"Знайдено записів: {len(records)}")
        for w in records:
            print_weather(w)


if __name__ == "__main__":
    main()
