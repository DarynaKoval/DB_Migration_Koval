"""Підключення до баз даних."""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def create_db_engine(url, **kwargs):
    """Те саме, що create_engine, але помилки PostgreSQL видно нормальним текстом.

    PostgreSQL на Windows пише помилки підключення українською (кодування
    Windows-1251), і драйвер psycopg2 замість них падає з UnicodeDecodeError.
    Тут ми перехоплюємо таку помилку і показуємо справжній текст.
    """
    url = make_url(url)
    if url.drivername != "postgresql+psycopg2":
        return create_engine(url, **kwargs)

    import psycopg2

    def connect():
        try:
            return psycopg2.connect(host=url.host or "localhost", port=url.port or 5432,
                                    user=url.username, password=url.password,
                                    dbname=url.database)
        except UnicodeDecodeError as e:
            message = e.object.decode("cp1251", errors="replace").strip()
            raise RuntimeError("PostgreSQL не пускає: " + message) from None

    return create_engine(url, creator=connect, **kwargs)


def ensure_database(url):
    """Створює базу даних, якщо її ще немає (щоб не робити це вручну)."""
    url = make_url(url)

    if url.get_backend_name() == "postgresql":
        server = create_db_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
        with server.connect() as conn:
            found = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :name"),
                                 {"name": url.database}).scalar()
            if not found:
                conn.execute(text(f'CREATE DATABASE "{url.database}"'))
                print("Створено базу", url.database)
        server.dispose()

    elif url.get_backend_name() == "mysql":
        server = create_db_engine(url.set(database=""))   # підключення без бази
        with server.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{url.database}`"))
            conn.commit()
        server.dispose()
