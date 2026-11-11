# Налаштування програми.
# Адреса бази: тип+драйвер://користувач:пароль@комп'ютер:порт/назва_бази
# Паролі: PostgreSQL - 1111, MySQL - 1234. Якщо в тебе інші - заміни тут.
# Базу weather_v8 програма створить сама під час alembic upgrade.
import os

POSTGRES_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/weather_v8"
MYSQL_URL = "mysql+pymysql://root:1234@localhost:3306/weather_v8?charset=utf8mb4"

# З якою базою працювати. За замовчуванням - PostgreSQL.
# Щоб працювати з MySQL, у PowerShell перед командами виконай:   $env:DB = "mysql"
# Щоб повернутися до PostgreSQL:                                $env:DB = ""
if os.environ.get("DB") == "mysql":
    DATABASE_URL = MYSQL_URL
else:
    DATABASE_URL = POSTGRES_URL

# Датасет лежить у корені проєкту
CSV_PATH = "GlobalWeatherRepository.csv"
