"""python scripts/load_csv.py GlobalWeatherRepository.csv  (після `alembic upgrade 001`)"""
import sys
from sqlalchemy import create_engine
from app.config import DATABASE_URL
from app.repositories.csv_loader import load_csv
print("Завантажено рядків:", load_csv(create_engine(DATABASE_URL), sys.argv[1]))
