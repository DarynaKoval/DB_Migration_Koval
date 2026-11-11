"""Етап 3: додати колонку go_outside ("Чи варто виходити на вулицю")

Revision ID: 003
Revises: 002
"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None

# Формула "Чи варто виходити на вулицю":
#   так - якщо час вимірювання між сходом і заходом сонця (світлий час доби);
#   так - якщо ніч, але освітленість місяця >= 75 %;
#   ні  - в усіх інших випадках.
# Цей SQL однаково працює і в PostgreSQL, і в MySQL.
FILL_SQL = """
UPDATE astronomy
SET go_outside = CASE
    WHEN (SELECT CAST(w.last_updated AS TIME) FROM weather w WHERE w.id = astronomy.weather_id)
         BETWEEN sunrise AND sunset THEN TRUE
    WHEN moon_illumination >= 75 THEN TRUE
    ELSE FALSE
END
"""


def upgrade():
    # Крок 1: додаємо колонку. Значення за замовчуванням немає,
    # тому в усіх існуючих рядках вона поки порожня (NULL).
    op.add_column("astronomy", sa.Column("go_outside", sa.Boolean, nullable=True))

    # Крок 2: заповнюємо всі існуючі рядки за формулою
    op.execute(FILL_SQL)

    # Крок 3: тепер, коли все заповнено, забороняємо порожні значення
    op.alter_column("astronomy", "go_outside", existing_type=sa.Boolean, nullable=False)


def downgrade():
    op.drop_column("astronomy", "go_outside")
