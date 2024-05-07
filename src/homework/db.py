# db.py
import logging
from os import environ

import psycopg
from psycopg import OperationalError, ProgrammingError, IntegrityError

from .exceptions import SaveException

database_logger = None


def setup_logger():
    global database_logger
    if not database_logger:
        database_logger = logging.getLogger(__name__)
        database_logger.setLevel(logging.INFO)
        handler = logging.FileHandler('database.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        database_logger.addHandler(handler)

database = environ["POSTGRES_DB"]
user = environ["POSTGRES_USER"]
password = environ["POSTGRES_PASSWORD"]

db_params = f"dbname={database} user={user} password={password} host=postgres-db"


def insert_currency(currency: str, price: float) -> None:
    setup_logger()
    try:
        with psycopg.connect(db_params) as conn:
            with conn.cursor() as cur:
                insert_query = "INSERT INTO crypto_prices (currency, price_usd) VALUES (%s, %s);"
                cur.execute(insert_query, (currency, price))
    except (OperationalError, ProgrammingError, IntegrityError) as e:
        database_logger.error(f"An error occurred during database insertion: {e}")
        raise SaveException
