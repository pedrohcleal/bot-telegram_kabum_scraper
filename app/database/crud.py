from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor, RealDictRow
from utils.telegram_api import mensagem_novo_valor_produto, novo_produto
import asyncio
from utils.sanitize import real_to_float
from database.crud_prices_hist import salve_hist


def insert_product(conn: psycopg2.extensions.connection, produto):
    print(f"insert produto on aws -> {produto}")
    salve_hist(conn, produto)
    # asyncio.run(novo_produto(produto))
    try:
        query = """
            INSERT INTO produtos_kabum.produtos (name, price, link, image, categoria)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            produto["name"],
            real_to_float(produto["price"]),
            produto["link"],
            produto["url_image"],
            produto["categoria"],
        )

        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()

        return True
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def have_product_in_bd(conn: psycopg2.extensions.connection, produto):
    try:
        query = """
            SELECT * FROM produtos_kabum.produtos
            WHERE name = %s AND link = %s
        """
        params = (produto["name"], produto["link"])
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result is not None
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def get_product(conn: psycopg2.extensions.connection, produto):
    try:
        query = """
            SELECT * FROM produtos_kabum.produtos
            WHERE name = %s AND link = %s
        """
        params = (produto["name"], produto["link"])
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def update_price(conn: psycopg2.extensions.connection, produto):
    print(f"update product on aws -> {produto}")
    salve_hist(conn, produto)
    old_produto: RealDictRow = get_product(conn, produto)
    valor_atual: float = real_to_float(produto["price"])
    valor_antigo: float = float(old_produto["price"])

    if valor_atual - valor_antigo < -50:
        asyncio.run(mensagem_novo_valor_produto(old_produto, produto))

    try:
        query = """
            UPDATE produtos_kabum.produtos SET price = %s
            WHERE name = %s AND link = %s
        """
        params = (
            real_to_float(produto["price"]),
            produto["name"],
            produto["link"],
        )
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.rowcount > 0:
                conn.commit()
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def deletar(conn: psycopg2.extensions.connection, produto):
    print(f"--->  Deletando linha do produto -> {produto} <---")
    try:
        query = """
            DELETE FROM produtos_kabum.produtos WHERE link = %s
        """
        params = (produto["link"],)
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if cursor.rowcount > 0:
                conn.commit()
                print("item deletado")
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e
