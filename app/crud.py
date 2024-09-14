from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from utils_telegram import mensagem_novo_valor_gpu, novo_produto
import asyncio
from utils import real_to_float


def insert_product(conn: psycopg2.extensions.connection, produto):
    print(f'insert produto on aws -> {produto}')
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
    print(f'update produto on aws -> {produto}')
    old_produt = get_product(conn, produto)
    if old_produt and real_to_float(produto["price"]) - real_to_float(old_produt["price"]) < -50:
        pass
        #asyncio.run(mensagem_novo_valor_gpu(old_gpu, gpu))

    try:
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")

        query = """
            UPDATE public.produtos SET price = %s, last_register_date = %s
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (produto["price"], date_now, produto["name"], produto["adm"], produto["link"])
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if cursor.rowcount > 0:
                conn.commit()
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def del_product(conn: psycopg2.extensions.connection, produto):
    print(f"-> Deletando produto da AWS RDS - {produto} <-")
    try:
        query = """
            DELETE FROM public.produtos WHERE link = %s
        """
        params = (produto["link"],)
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if cursor.rowcount > 0:
                conn.commit()
                print("- item deletado -")
                return True
            raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e
