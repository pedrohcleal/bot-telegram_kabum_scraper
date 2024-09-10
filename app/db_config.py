import os
from typing import Generator
from contextlib import contextmanager
import sqlite3


DATABASE: str = os.path.join(os.path.dirname(__file__), "kabum.db")


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn: sqlite3.Connection = sqlite3.connect(DATABASE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        raise
    finally:
        conn.close()
