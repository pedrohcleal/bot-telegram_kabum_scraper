import os
from collections.abc import Generator
from contextlib import contextmanager
import sqlite3

DATABASE_PATH = os.getenv("database_path", 'KabumDatabase.db')

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Configura o cursor para retornar dicionários
        yield conn
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        raise
    finally:
        if conn:
            conn.close()
