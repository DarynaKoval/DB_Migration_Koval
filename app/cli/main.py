"""Presentation шар (консоль). Приклад: python -m app.cli.main Ukraine 2024-05-16 --location Kyiv"""
import argparse
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import DATABASE_URL
from app.repositories.weather_repo import WeatherRepository
from app.services.weather_service import WeatherService

def main():
    p = argparse.ArgumentParser()
    p.add_argument("country"); p.add_argument("date", type=date.fromisoformat)
    p.add_argument("--location")
    a = p.parse_args()
    with Session(create_engine(DATABASE_URL)) as s:
        res = WeatherService(WeatherRepository(s)).report(a.country, a.date, a.location)
    for r in res: print(r)
    if not res: print("Даних немає")

if __name__ == "__main__": main()
