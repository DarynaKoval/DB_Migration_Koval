"""Завдання 5: перенести дані з PostgreSQL у MySQL і перевірити, що бази однакові.

Спочатку на MySQL треба накотити ті самі міграції:
    $env:DB = "mysql"
    alembic upgrade head
    $env:DB = ""
Потім:
    python scripts/copy_db.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import MetaData, Table, func, select, text

from app.config import MYSQL_URL, POSTGRES_URL
from app.db import create_db_engine

TABLES = ["weather", "astronomy"]   # спочатку батьківська таблиця, потім залежна
BATCH_SIZE = 5000

CHECKS = [
    ("Рядків у weather", "SELECT COUNT(*) FROM weather"),
    ("Рядків у astronomy", "SELECT COUNT(*) FROM astronomy"),
    ("Виходити = так", "SELECT COUNT(*) FROM astronomy WHERE go_outside = TRUE"),
    ("Виходити = ні", "SELECT COUNT(*) FROM astronomy WHERE go_outside = FALSE"),
    ("Сума освітленості", "SELECT SUM(moon_illumination) FROM astronomy"),
    ("Версія міграції", "SELECT version_num FROM alembic_version"),
]

src = create_db_engine(POSTGRES_URL)
dst = create_db_engine(MYSQL_URL)

# 1) копіюємо таблиці пачками
for name in TABLES:
    s = Table(name, MetaData(), autoload_with=src)
    d = Table(name, MetaData(), autoload_with=dst)
    with dst.connect() as conn:
        if conn.execute(select(func.count()).select_from(d)).scalar() > 0:
            print(f"У MySQL таблиця {name} вже не порожня - копіювання пропускаю.")
            continue
    copied = 0
    with src.connect() as a, dst.begin() as b:
        result = a.execute(select(s).order_by(s.c.id)).mappings()
        while rows := result.fetchmany(BATCH_SIZE):
            b.execute(d.insert(), [dict(r) for r in rows])
            copied += len(rows)
            print(f"  {name}: {copied}", end="\r")
    print(f"Скопійовано {name}: {copied}")

# 2) порівнюємо дві бази
print()
print(f"{'Перевірка':22} {'PostgreSQL':>12} {'MySQL':>12}")
with src.connect() as a, dst.connect() as b:
    for title, sql in CHECKS:
        x = a.execute(text(sql)).scalar()
        y = b.execute(text(sql)).scalar()
        result = "однаково" if str(x) == str(y) else "РІЗНИЦЯ!"
        print(f"{title:22} {x!s:>12} {y!s:>12}   {result}")
