"""Етап 1: одна таблиця weather (вітер усередині)"""
import sqlalchemy as sa
from alembic import op

revision, down_revision = "001", None
DIRS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

def upgrade():
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("location_name", sa.String(150), nullable=False),
        sa.Column("last_updated", sa.DateTime, nullable=False),
        sa.Column("sunrise", sa.Time),
        sa.Column("wind_mph", sa.Float), sa.Column("wind_kph", sa.Float),
        sa.Column("wind_degree", sa.Integer),
        sa.Column("wind_direction", sa.Enum(*DIRS, name="wind_direction")),
        sa.Column("gust_mph", sa.Float), sa.Column("gust_kph", sa.Float),
    )
    op.create_index("ix_weather_country_date", "weather", ["country", "last_updated"])

def downgrade():
    op.drop_table("weather")
    op.execute("DROP TYPE IF EXISTS wind_direction") if op.get_bind().dialect.name == "postgresql" else None
