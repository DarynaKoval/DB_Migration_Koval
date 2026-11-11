"""Завантаження CSV у таблицю weather.

Дані завантажуються ОДИН раз - на початку, коли база в стані міграції 001
(одна таблиця weather). Далі міграції 002 і 003 переробляють уже наповнену
базу - так видно, що міграції не втрачають дані.
"""
import csv
from datetime import datetime

from sqlalchemy import MetaData, Table, func, select

from app.models.orm import MOON_PHASES, WIND_DIRECTIONS

BATCH_SIZE = 5000


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def to_int(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def to_time(value):
    # У CSV час записаний як "04:50 AM". Інколи там "No moonrise",
    # "Does not set today", "****" тощо - тоді записуємо порожнє значення.
    try:
        return datetime.strptime(value.strip(), "%I:%M %p").time()
    except (ValueError, AttributeError):
        return None


def to_enum(value, allowed):
    value = (value or "").strip()
    return value if value in allowed else None


def convert(row):
    """Один рядок CSV -> словник з потрібними колонками і правильними типами."""
    return {
        "country": row["country"],
        "location_name": row["location_name"],
        "last_updated": datetime.strptime(row["last_updated"], "%Y-%m-%d %H:%M"),
        "temperature_celsius": to_float(row["temperature_celsius"]),
        "condition_text": row["condition_text"],
        "wind_kph": to_float(row["wind_kph"]),
        "wind_degree": to_int(row["wind_degree"]),
        "wind_direction": to_enum(row["wind_direction"], WIND_DIRECTIONS),
        "sunrise": to_time(row["sunrise"]),
        "sunset": to_time(row["sunset"]),
        "moonrise": to_time(row["moonrise"]),
        "moonset": to_time(row["moonset"]),
        "moon_phase": to_enum(row["moon_phase"], MOON_PHASES),
        "moon_illumination": to_int(row["moon_illumination"]),
    }


def load_csv(engine, path):
    # беремо таблицю weather такою, якою вона є в базі зараз
    table = Table("weather", MetaData(), autoload_with=engine)

    if "sunrise" not in table.c:
        raise RuntimeError("Дані завантажуються, коли база на міграції 001.\n"
                           "Виконай: alembic downgrade base, потім alembic upgrade 001")

    with engine.begin() as conn:
        if conn.execute(select(func.count()).select_from(table)).scalar() > 0:
            raise RuntimeError("У таблиці weather вже є дані - повторно не завантажую.")

        total, batch = 0, []
        with open(path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                batch.append(convert(row))
                if len(batch) == BATCH_SIZE:
                    conn.execute(table.insert(), batch)
                    total += len(batch)
                    print("Завантажено:", total)
                    batch = []
        if batch:
            conn.execute(table.insert(), batch)
            total += len(batch)
    return total
