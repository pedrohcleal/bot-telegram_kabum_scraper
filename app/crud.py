from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from utils.utils_telegram import mensagem_novo_valor_gpu, novo_produto
import asyncio
from utils.utils import real_to_float
from crud_prices_hist import salve_hist


def insert_product(conn: psycopg2.extensions.connection, produto):
    print(f"insert produto on aws -> {produto}")
    salve_hist(conn, produto)
    # asyncio.run(novo_produto(produto))
    try:
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO public.produtos (name, adm, price, link, last_register_date, image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            produto["name"],
            produto["adm"],
            produto["price"],
            produto["link"],
            date_now,
            produto["url_image"],
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
            SELECT * FROM public.produtos
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (produto["name"], produto["adm"], produto["link"])
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
            SELECT * FROM public.produtos
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (produto["name"], produto["adm"], produto["link"])
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def update_price(conn: psycopg2.extensions.connection, produto):
    print(f"update gpu on aws -> {produto}")
    salve_hist(conn, produto)
    old_produto = get_product(conn, produto)
    if (
        old_produto
        and real_to_float(produto["price"]) - real_to_float(old_produto["price"]) < -50
    ):
        asyncio.run(mensagem_novo_valor_gpu(old_produto, produto))

    try:
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")

        query = """
            UPDATE public.produtos SET price = %s, last_register_date = %s
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (
            produto["price"],
            date_now,
            produto["name"],
            produto["adm"],
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
            DELETE FROM public.produtos WHERE link = %s
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
