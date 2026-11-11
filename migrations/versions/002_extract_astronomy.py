"""Етап 2: винести схід/захід сонця і місяця в окрему таблицю astronomy

Revision ID: 002
Revises: 001
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

MOON_PHASES = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
               "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]

# колонки, які переїжджають з weather в astronomy
COLUMNS = ["sunrise", "sunset", "moonrise", "moonset", "moon_phase", "moon_illumination"]


def moon_phase_type():
    # У Postgres тип moon_phase_enum вже створений на етапі 1 - вдруге не створюємо.
    # У MySQL enum - просто тип колонки, там нічого особливого не треба.
    return sa.Enum(*MOON_PHASES, name="moon_phase_enum").with_variant(
        postgresql.ENUM(*MOON_PHASES, name="moon_phase_enum", create_type=False),
        "postgresql",
    )


def upgrade():
    # Крок 1: створюємо нову таблицю
    op.create_table(
        "astronomy",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("weather_id", sa.Integer, sa.ForeignKey("weather.id"),
                  nullable=False, unique=True),
        sa.Column("sunrise", sa.Time),
        sa.Column("sunset", sa.Time),
        sa.Column("moonrise", sa.Time),
        sa.Column("moonset", sa.Time),
        sa.Column("moon_phase", moon_phase_type()),
        sa.Column("moon_illumination", sa.Integer),
    )

    # Крок 2: копіюємо дані зі старої таблиці в нову
    cols = ", ".join(COLUMNS)
    op.execute(f"INSERT INTO astronomy (weather_id, {cols}) SELECT id, {cols} FROM weather")

    # Крок 3: тільки тепер видаляємо старі колонки - дані вже скопійовані
    for col in COLUMNS:
        op.drop_column("weather", col)


def downgrade():
    # Повернення назад теж без втрати даних:
    # повертаємо колонки -> копіюємо дані назад -> видаляємо astronomy
    op.add_column("weather", sa.Column("sunrise", sa.Time))
    op.add_column("weather", sa.Column("sunset", sa.Time))
    op.add_column("weather", sa.Column("moonrise", sa.Time))
    op.add_column("weather", sa.Column("moonset", sa.Time))
    op.add_column("weather", sa.Column("moon_phase", moon_phase_type()))
    op.add_column("weather", sa.Column("moon_illumination", sa.Integer))

    for col in COLUMNS:
        op.execute(f"UPDATE weather SET {col} = "
                   f"(SELECT a.{col} FROM astronomy a WHERE a.weather_id = weather.id)")

    op.drop_table("astronomy")
