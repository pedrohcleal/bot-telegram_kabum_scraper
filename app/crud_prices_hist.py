from crud import get_product
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime


def salvar_historico_produto(conn: psycopg2.extensions.connection, produto):
    print("salvando_historico")
    last_produto = get_ultimo_historico_produto(conn, produto)
    now = datetime.now()
    date_now = now.strftime("%Y-%m-%d %H:%M:%S")  # Formato padrão para PostgreSQL
    try:
        query = """
            INSERT INTO public.produto_hist (nome, link, dt_start, dt_end)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            produto["nome"],
            produto["link"],
            last_produto["last_register_date"],
            date_now,
        )
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        return True
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def get_ultimo_historico_produto(conn: psycopg2.extensions.connection, produto):
    last_produto = get_product(conn, produto)
    now = datetime.now()
    date_now = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        query = """
            SELECT * FROM public.produto_hist WHERE link = %s ORDER BY dt_end DESC
        """
        params = (produto["link"],)
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e
