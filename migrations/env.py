import os
from alembic import context
from sqlalchemy import create_engine

url = os.environ["DATABASE_URL"]  # postgresql+psycopg2://... або mysql+pymysql://...

if context.is_offline_mode():
    context.configure(url=url, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with create_engine(url).connect() as conn:
        context.configure(connection=conn)
        with context.begin_transaction():
            context.run_migrations()
        conn.commit()
