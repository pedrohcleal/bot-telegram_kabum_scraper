import os
import sqlite3
import pytest
from utils.awin_api import create_affiliate_link
from utils.telegram_api import test_envio_mensagem_grupo
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis de ambiente
telegram_token = os.getenv('TELEGRAM_TOKEN')
id_group = os.getenv('ID_GROUP')
access_token = os.getenv('access_token')
advertiser_id = os.getenv('advertiser_id')
publisher_id = os.getenv('publisher_id')
database_path = os.getenv('database_path')

# Função para verificar se as variáveis de ambiente foram carregadas corretamente
def test_env_vars():
    assert telegram_token, "Erro: TELEGRAM_TOKEN não definido"
    assert id_group, "Erro: ID_GROUP não definido"
    assert access_token, "Erro: access_token não definido"
    assert advertiser_id, "Erro: advertiser_id não definido"
    assert publisher_id, "Erro: publisher_id não definido"
    assert database_path, "Erro: database_path não definido"

    print(f"TELEGRAM_TOKEN: {telegram_token}")
    print(f"ID_GROUP: {id_group}")
    print(f"access_token: {access_token}")
    print(f"advertiser_id: {advertiser_id}")
    print(f"publisher_id: {publisher_id}")
    print(f"database_path: {database_path}")

# Teste de envio de mensagem no Telegram
@pytest.mark.asyncio
async def test_telegram():
    await test_envio_mensagem_grupo()

# Teste de banco de dados SQLite
def test_bd():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)''')

    # Inserir dados de teste
    cursor.execute("INSERT INTO test_table (name) VALUES ('Teste')")
    conn.commit()

    # Consultar os dados
    cursor.execute("SELECT * FROM test_table")
    results = cursor.fetchall()

    # Verificar se a inserção foi bem-sucedida
    assert len(results) > 0, "Nenhum dado encontrado no banco de dados"

    # Fechar a conexão
    conn.close()

# Teste de criação de link de afiliado
def test_awin():
    original_url = "https://www.kabum.com.br/"
    affiliate_link = create_affiliate_link(original_url=original_url)
    assert affiliate_link, "Erro: Não foi possível criar o link de afiliado"
    print(f"Link de afiliado: '{affiliate_link}'")

async def run_all_tests():
    test_awin()
    await test_envio_mensagem_grupo()
    test_bd()
    test_env_vars()
    await test_telegram()