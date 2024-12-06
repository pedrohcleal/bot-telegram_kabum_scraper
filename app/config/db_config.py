import os
from typing import Generator
from contextlib import contextmanager
import psycopg2
from psycopg2 import OperationalError

HOST = os.getenv("host")
PORT = os.getenv("port")
USER = os.getenv("principaluser")
PASSWORD = os.getenv("senha")
DATABASE = os.getenv("database")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    conn: psycopg2.extensions.connection
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = (
            True  # Necessário para operações que não precisam de commit explícito
        )
        yield conn
    except OperationalError as e:
        print(f"DB Error: {e}")
        raise
    finally:
        if conn:
            conn.close()
