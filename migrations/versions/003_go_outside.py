"""Етап 3: колонка go_outside у 3 кроки: додати NULL -> заповнити -> NOT NULL"""
import sqlalchemy as sa
from alembic import op

revision, down_revision = "003", "002"
MAX_KPH = 36  # 10 м/с

def upgrade():
    op.add_column("wind", sa.Column("go_outside", sa.Boolean, nullable=True))
    op.execute(f"UPDATE wind SET go_outside = CASE WHEN wind_kph IS NOT NULL AND wind_kph <= {MAX_KPH} THEN TRUE ELSE FALSE END")
    op.alter_column("wind", "go_outside", existing_type=sa.Boolean, nullable=False)  # без default

def downgrade():
    op.drop_column("wind", "go_outside")
