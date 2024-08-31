from datetime import datetime
import sqlite3

def insert_gpu(conn: sqlite3.Connection, gpu):
    try:
        now = datetime.now()
        date_now = now.strftime('%Y/%m/%d %H:%M:%S')
        query = """
            INSERT INTO gpus_prices (name, adm, price, link, last_register_date)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (gpu['name'], gpu['adm'], gpu['price'], gpu['link'], date_now)
        
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
        params = (gpu['name'], gpu['adm'], gpu['link'])
        con_exec = conn.execute(query, params)
        result = con_exec.fetchone()
        if result:
            print('HAVE IN BD')
            return True
        return False
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e
    

def get_gpu_price(conn: sqlite3.Connection, gpu):
    try:
        query = """
            SELECT * FROM gpus_prices 
            WHERE name = ? AND adm = ? AND link = ?
        """
        params = (gpu['name'], gpu['adm'], gpu['link'])
        con_exec = conn.execute(query, params)
        result = con_exec.fetchone()
        if result:
            return result[2]
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e
    
def update_gpu_price(conn: sqlite3.Connection, gpu):
    try:
        now = datetime.now()
        date_now = now.strftime('%Y/%m/%d %H:%M:%S')
        
        query = """
            UPDATE gpus_prices SET price = ?, last_register_date = ? WHERE name = ? AND adm = ? AND link = ? 
        """
        params = (gpu['price'], date_now, gpu['name'], gpu['adm'], gpu['link'])
        cursor = conn.execute(query, params)
        
        if cursor.rowcount == 1:  
            conn.commit() 
            return True
        else:
            raise ValueError('Qtd de linhas afetadas != 1, verificar...')
    
    except sqlite3.Error as e:
        print(f"SQL error = {e}")
        raise e
    