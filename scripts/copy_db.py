"""Етап 5: копіює дані Postgres -> MySQL. Спочатку `alembic upgrade head` на цільовій БД.
python scripts/copy_db.py <SRC_URL> <DST_URL>"""
import sys
from sqlalchemy import MetaData, Table, create_engine, select
src, dst = create_engine(sys.argv[1]), create_engine(sys.argv[2])
for name in ("weather", "wind"):  # порядок: спочатку батьківська таблиця
    s, d = Table(name, MetaData(), autoload_with=src), Table(name, MetaData(), autoload_with=dst)
    with src.connect() as a, dst.begin() as b:
        res = a.execute(select(s)).mappings()
        while chunk := res.fetchmany(1000):
            b.execute(d.insert(), [dict(r) for r in chunk])
    print("скопійовано", name)
