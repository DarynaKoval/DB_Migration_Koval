import os
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:1111@localhost/weather")
