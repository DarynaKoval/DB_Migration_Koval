"""Завантаження CSV. Працює через reflection, тому підходить для будь-якого етапу схеми."""
import csv
from datetime import datetime
from sqlalchemy import MetaData, Table

def _num(v, cast): return cast(v) if v not in ("", None) else None
def _time(v):
    try: return datetime.strptime(v, "%I:%M %p").time()
    except (ValueError, TypeError): return None

def load_csv(engine, path: str, batch: int = 1000) -> int:
    table = Table("weather", MetaData(), autoload_with=engine)
    cols = set(table.c.keys())
    n, rows = 0, []
    with engine.begin() as conn, open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            row = {"country": r["country"], "location_name": r["location_name"],
                   "last_updated": datetime.strptime(r["last_updated"], "%Y-%m-%d %H:%M"),
                   "sunrise": _time(r.get("sunrise")),
                   "wind_mph": _num(r["wind_mph"], float), "wind_kph": _num(r["wind_kph"], float),
                   "wind_degree": _num(r["wind_degree"], int), "wind_direction": r["wind_direction"] or None,
                   "gust_mph": _num(r["gust_mph"], float), "gust_kph": _num(r["gust_kph"], float)}
            rows.append({k: v for k, v in row.items() if k in cols}); n += 1
            if len(rows) == batch: conn.execute(table.insert(), rows); rows = []
        if rows: conn.execute(table.insert(), rows)
    return n
