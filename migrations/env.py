# Налаштування Alembic: звідки брати адресу бази.
import os
import sys
from logging.config import fileConfig

from alembic import context

# щоб Alembic бачив папку app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import DATABASE_URL
from app.db import create_db_engine, ensure_database

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)   # щоб у консолі було видно, що робиться

if context.is_offline_mode():
    # "alembic upgrade head --sql" - тільки показати SQL, без підключення
    context.configure(url=DATABASE_URL, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    ensure_database(DATABASE_URL)          # створити базу, якщо її ще немає
    engine = create_db_engine(DATABASE_URL)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
