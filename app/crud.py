from datetime import datetime
import sqlite3
from telegram_main import mensagem_novo_valor_gpu, novo_produto
import asyncio
from utils import real_to_float

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
        return result
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e


def update_gpu_price(conn: sqlite3.Connection, gpu):
    old_gpu = get_gpu(conn, gpu)
    if real_to_float(gpu["price"]) - real_to_float(old_gpu["price"]) < -39:
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
        params = (produto["link"],)
        cursor = conn.execute(query, params)

        if cursor.rowcount > 0:
            conn.commit()
            print('item deletado')
            return True
        raise ValueError("Qtd de linhas afetadas = 0, verificar...")

    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e
