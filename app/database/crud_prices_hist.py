import psycopg2
from psycopg2 import OperationalError
from datetime import datetime


def salve_hist(conn: psycopg2.extensions.connection, produto) -> None:
    print("salvando_historico")
    now: datetime = datetime.now()
    date_now: str = now.strftime("%Y-%m-%d %H:%M:%S")  # Formato padrão para PostgreSQL
    try:
        query = """
            INSERT INTO public.produtos_hist (nome, link, price, register_date)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            produto["name"],
            produto["link"],
            produto["price"],
            date_now,
        )
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


def get_last_5prices(conn: psycopg2.extensions.connection, produto):
    print("Veficando últimos preços na aws")
    try:
        query = """
            SELECT DISTINCT price
            FROM public.produtos_hist
            WHERE link = %s AND price NOT LIKE '%%x%%'
            LIMIT 6;
        """
        params = (produto["link"],)
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result: list[tuple[str]] = cursor.fetchall()
            print(f"result = {result}")
            print(f"type result = {type(result)}")

        if not result:
            return "sem histórico no momento..."
        return ", ".join([x[0] for x in result])
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e
