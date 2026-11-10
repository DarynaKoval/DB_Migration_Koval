"""Етап 2: рефакторинг — дані про вітер переносяться в таблицю wind"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision, down_revision = "002", "001"
DIRS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
COLS = ["wind_mph", "wind_kph", "wind_degree", "wind_direction", "gust_mph", "gust_kph"]

def upgrade():
    # тип enum у Postgres уже створено на етапі 1 — повторно не створюємо
    direction = sa.Enum(*DIRS, name="wind_direction").with_variant(
        postgresql.ENUM(*DIRS, name="wind_direction", create_type=False), "postgresql")
    op.create_table(
        "wind",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("weather_id", sa.Integer, sa.ForeignKey("weather.id"), nullable=False, unique=True),
        sa.Column("wind_mph", sa.Float), sa.Column("wind_kph", sa.Float),
        sa.Column("wind_degree", sa.Integer), sa.Column("wind_direction", direction),
        sa.Column("gust_mph", sa.Float), sa.Column("gust_kph", sa.Float),
    )
    # 1) копіюємо дані, 2) лише потім видаляємо старі колонки — дані не втрачаються
    op.execute(f"INSERT INTO wind (weather_id, {', '.join(COLS)}) SELECT id, {', '.join(COLS)} FROM weather")
    for c in COLS:
        op.drop_column("weather", c)
