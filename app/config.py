# Налаштування програми.
# Адреса бази: тип+драйвер://користувач:пароль@комп'ютер:порт/назва_бази
# Пароль PostgreSQL - 1111. Якщо в тебе інший - заміни тут.
# Базу weather_v8 програма створить сама під час alembic upgrade.
DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/weather_v8"

# Датасет лежить у корені проєкту
CSV_PATH = "GlobalWeatherRepository.csv"
