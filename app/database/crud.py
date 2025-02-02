import sqlite3
from sqlite3 import Error
from utils.telegram_api import mensagem_novo_valor_produto
import asyncio
from database.crud_prices_hist import salve_hist

def insert_product(conn: sqlite3.Connection, produto):
    print(f"insert produto -> {produto['link']}")
    salve_hist(conn, produto)
    try:
        query = """
            INSERT INTO produtos (id, name, price, link, image, categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (
            produto['id'],
            produto["name"],
            produto["price"],
            produto["link"],
            produto["url_image"],
            produto["categoria"],
        )

        with conn:  # Autocommit enabled
            conn.execute(query, params)

        return True
    except Error as e:
        print(f"SQL error = {e}, product = {produto}")
        raise e

def have_product_in_bd(conn: sqlite3.Connection, produto):
    try:
        query = """
            SELECT * FROM produtos
            WHERE id = ?
        """
        params = (produto["id"], )
        cursor = conn.execute(query, params)
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"SQL error = {e} , produto: {produto}")
        raise e

def get_product(conn: sqlite3.Connection, produto):
    try:
        query = """
            SELECT * FROM produtos
            WHERE name = ? AND link = ?
        """
        params = (produto["name"], produto["link"])
        cursor = conn.execute(query, params)
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"SQL error = {e}")
        raise e
    
def get_product_from_hist(conn: sqlite3.Connection, produto):
    try:
        query = """
           SELECT * FROM produtos_hist
            WHERE id = ?
            ORDER BY register_date ASC
        """
        params = (produto["id"], )
        cursor = conn.execute(query, params)
        result = cursor.fetchone()
        print(f'old_produto_from_hist = {result}')
        return result
    except Error as e:
        print(f"SQL error = {e}")
        raise e

def update_price(conn: sqlite3.Connection, produto):
    print(f"update product -> {produto['link']}")
    salve_hist(conn, produto)
    
    old_produto = get_product(conn, produto)
    
    valor_atual: float = produto["price"]
    valor_antigo: float = old_produto["price"]
    
    if valor_atual - valor_antigo < -100:
        print(f'ID do produto {produto['id']}')
        asyncio.run(
            mensagem_novo_valor_produto(old_produto=old_produto, produto=produto)
        )
    
    try:
        query = """
            UPDATE produtos SET name = ?, price = ?, link = ?, image = ?, categoria = ?
            WHERE id = ?
        """
        params = (
            produto["name"],
            produto["price"],
            produto["link"],
            produto["url_image"],
            produto["categoria"],
            produto['id']
        )
        with conn:
            cursor = conn.execute(query, params)
            if cursor.rowcount > 0:
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except Error as e:
        print(f"SQL error = {e}")
        raise e

def deletar(conn: sqlite3.Connection, produto):
    print(f"--->  Deletando linha do produto -> {produto['link']} <---")
    try:
        query = """
            DELETE FROM produtos WHERE link = ?
        """
        params = (produto["link"],)
        with conn:  # Autocommit enabled
            cursor = conn.execute(query, params)

            if cursor.rowcount > 0:
                print("item deletado")
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except Error as e:
        print(f"SQL error = {e}")
        raise e
