from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from utils_telegram import mensagem_novo_valor_gpu, novo_produto
import asyncio
from utils import real_to_float


def insert_gpu(conn: psycopg2.extensions.connection, gpu):
    print(f'insert produto on aws -> {gpu}')
    # asyncio.run(novo_produto(gpu))
    try:
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO public.produtos (name, adm, price, link, last_register_date, image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            gpu["name"],
            gpu["adm"],
            gpu["price"],
            gpu["link"],
            date_now,
            gpu["url_image"],
        )

        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()

        return True
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def gpu_have_in_bd(conn: psycopg2.extensions.connection, gpu):
    try:
        query = """
            SELECT * FROM public.produtos
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (gpu["name"], gpu["adm"], gpu["link"])
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result is not None
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def get_gpu(conn: psycopg2.extensions.connection, gpu):
    try:
        query = """
            SELECT * FROM public.produtos
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (gpu["name"], gpu["adm"], gpu["link"])
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def update_gpu_price(conn: psycopg2.extensions.connection, gpu):
    print(f'update gpu on aws -> {gpu}')
    old_gpu = get_gpu(conn, gpu)
    if old_gpu and real_to_float(gpu["price"]) - real_to_float(old_gpu["price"]) < -50:
        pass
        #asyncio.run(mensagem_novo_valor_gpu(old_gpu, gpu))

    try:
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")

        query = """
            UPDATE public.produtos SET price = %s, last_register_date = %s
            WHERE name = %s AND adm = %s AND link = %s
        """
        params = (gpu["price"], date_now, gpu["name"], gpu["adm"], gpu["link"])
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
