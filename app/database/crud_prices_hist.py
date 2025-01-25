import sqlite3
from sqlite3 import Error
from datetime import datetime

def salve_hist(conn: sqlite3.Connection, produto) -> None:
    print("salvando_historico")
    now: datetime = datetime.now()
    date_now: str = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        query = """
            INSERT INTO produtos_hist (id, nome, link, price, register_date, categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (
            produto['id'],
            produto["name"],
            produto["link"],
            produto["price"],
            date_now,
            produto["categoria"],

        )
        with conn:  # Autocommit enabled
            conn.execute(query, params)

    except Error as e:
        print(f"SQL error = {e}")
        raise e

def get_last_5prices(conn: sqlite3.Connection, produto) -> str:
    print("Verificando últimos preços")
    try:
        query = """
            SELECT DISTINCT price
            FROM produtos_hist
            WHERE link = ? AND price != ?
            ORDER BY price ASC
            LIMIT 6;
        """
        params = (produto["link"], produto["price"])
        cursor = conn.execute(query, params)
        result = cursor.fetchall()
        print(f"result = {result}")
        print(f"type result = {type(result)}")

        if not result:
            return "sem histórico no momento..."
        return ", R$".join([str(x[0]) for x in result])
    except Error as e:
        print(f"SQL error = {e}")
        raise e