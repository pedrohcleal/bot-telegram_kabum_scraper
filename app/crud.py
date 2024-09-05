from datetime import datetime
import sqlite3
from telegram_main import enviar_mensagem, mensagem_novo_valor_gpu, novo_produto
import asyncio
import requests
from bs4 import BeautifulSoup as bs4
from db_config import get_db_connection
from time import sleep

def insert_gpu(conn: sqlite3.Connection, gpu):
    asyncio.run(novo_produto(gpu))
    try:
        now = datetime.now()
        date_now = now.strftime("%Y/%m/%d %H:%M:%S")
        query = """
            INSERT INTO gpus_prices (name, adm, price, link, last_register_date, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (gpu["name"], gpu["adm"], gpu["price"], gpu["link"], date_now, gpu["url_image"])

        conn.execute(query, params)
        conn.commit()

        return True
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e


def gpu_have_in_bd(conn: sqlite3.Connection, gpu):
    try:
        query = """
            SELECT * FROM gpus_prices
            WHERE name = ? AND adm = ? AND link = ?
        """
        params = (gpu["name"], gpu["adm"], gpu["link"])
        con_exec = conn.execute(query, params)
        result = con_exec.fetchone()
        if result:
            return True
        return False
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e


def get_gpu(conn: sqlite3.Connection, gpu):
    try:
        query = """
            SELECT * FROM gpus_prices
            WHERE name = ? AND adm = ? AND link = ?
        """
        params = (gpu["name"], gpu["adm"], gpu["link"])
        con_exec = conn.execute(query, params)
        result = con_exec.fetchone()
        if result:
            return {
                "id":result[0], 
                "name":result[1], 
                "price": result[2], 
                "link": result[3], 
                "last_register_date": result[4], 
                "adm": result[5]
                }
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e


def update_gpu_price(conn: sqlite3.Connection, gpu):
    old_gpu = get_gpu(conn, gpu)
    if int(gpu["price"].replace("R$", '').replace(",",'.').strip()) < int(old_gpu["price"].replace("R$", '').replace(",",'.').strip()):
        asyncio.run(mensagem_novo_valor_gpu(old_gpu, gpu))
    
    try:
        now = datetime.now()
        date_now = now.strftime("%Y/%m/%d %H:%M:%S")

        query = """
            UPDATE gpus_prices SET price = ?, last_register_date = ? WHERE name = ? AND adm = ? AND link = ?
        """
        params = (gpu["price"], date_now, gpu["name"], gpu["adm"], gpu["link"])
        cursor = conn.execute(query, params)

        if cursor.rowcount > 0:
            conn.commit()
            return True
        raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e

def deletar(conn: sqlite3.Connection, produto):
    print(f'--->  Deletando linha do produto -> {produto} <---')
    try:
        query = """
            DELETE FROM gpus_prices WHERE link = ?
        """
        params = (produto[3],)
        cursor = conn.execute(query, params)

        if cursor.rowcount > 0:
            conn.commit()
            print('item deletado')
            return True
        raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e

def verificar_banco(conn: sqlite3.Connection):
    seletor = "finalPrice"
    query = "SELECT * FROM gpus_prices"
    try:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        for produto in rows:
            sleep(0.5)
            print(f'verificando - > {produto[3]}')
            response = requests.get(produto[3])
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
    with get_db_connection() as conn:
        verificar_banco(conn)