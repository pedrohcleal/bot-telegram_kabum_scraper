from crud import get_gpu
import sqlite3
from datetime import datetime


def salvar_historico_produto(conn: sqlite3.Connection, produto):
    print('salvando_historico')
    last_produto = get_ultimo_historico_produto(conn, produto)
    now = datetime.now()
    date_now = now.strftime("%Y/%m/%d %H:%M:%S")
    try:
        query = """
            INSERT INTO prices_hist (nome, link, dt_start, dt_end)
            VALUES (?, ?, ?, ?)
        """
        params = (produto["nome"], produto["link"], last_produto["last_register_date"], date_now)
        conn.execute(query, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e

def get_ultimo_historico_produto(conn: sqlite3.Connection, produto):
    last_produto = get_gpu(conn, produto)
    now = datetime.now()
    date_now = now.strftime("%Y/%m/%d %H:%M:%S")
    try:
        query = """
            SELECT * FROM prices_hist WHERE link = ? ORDER BY DATE(dt_end)
        """
        params = (produto["link"], last_produto["last_register_date"], date_now)
        cursor: sqlite3.Cursor = conn.execute(query, params)
        result = cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e