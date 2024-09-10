from db_config import get_db_connection
import sqlite3, requests
from bs4 import BeautifulSoup as bs4
from time import sleep
from crud import deletar

def verificar_banco(conn: sqlite3.Connection):
    seletor = "finalPrice"
    query = "SELECT * FROM gpus_prices"
    try:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        for produto in rows:
            sleep(0.5)
            print(f'verificando - > {produto["link"]}')
            response = requests.get(produto["link"])
            if response.status_code == 200:
                soup = bs4(response.text, "html.parser")
                if not soup.find(class_=seletor):
                    with get_db_connection() as conn:
                        deletar(conn, produto)
            else:
                print(f'link incorreto, Produto -> {produto}')
                break
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e
    
    
if __name__ == "__main__":
    while True:
        with get_db_connection() as conn:
            verificar_banco(conn)