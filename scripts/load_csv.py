"""Завантажити CSV у базу (після `alembic upgrade 001`).

Запуск:  python scripts/load_csv.py
"""
import os
import sys

# щоб скрипт бачив папку app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import CSV_PATH, DATABASE_URL
from app.db import create_db_engine
from app.repositories.csv_loader import load_csv

print("База даних:", DATABASE_URL.split(":")[0])
print("Читаю", CSV_PATH)
try:
    total = load_csv(create_db_engine(DATABASE_URL), CSV_PATH)
    print("Готово! Всього рядків:", total)
except RuntimeError as e:
    print(e)
