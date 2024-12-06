import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
import requests
from bs4 import BeautifulSoup as bs4
from time import sleep
from database.crud import deletar
from config.db_config import get_db_connection


def verificar_banco(conn: psycopg2.extensions.connection):
    seletor = "finalPrice"
    query = "SELECT DISTINCT(link) FROM produtos_kabum.produtos"
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"quantidade produtos a serem verificados = {len(rows)}")
            for produto in rows:
                print(f'verificando -> {produto["link"]}')
                response = requests.get(produto["link"])
                if response.status_code == 200:
                    soup = bs4(response.text, "html.parser")
                    if not soup.find(class_=seletor):
                        with get_db_connection() as conn:
                            deletar(conn, produto)
                else:
                    print(f"link incorreto, Produto -> {produto}")
                    break
                sleep(3)
    except OperationalError as e:
        print(f"SQL error = {e}")
        raise e


if __name__ == "__main__":
    while True:
        with get_db_connection() as conn:
            verificar_banco(conn)
