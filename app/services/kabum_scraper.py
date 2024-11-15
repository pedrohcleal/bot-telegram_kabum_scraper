from database.crud import insert_product, have_product_in_bd, get_product, update_price
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config.db_config import get_db_connection
from pprint import pprint
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


NEXT_BUTTON_SELECTOR = "#listingPagination > ul > li.next > a"
COOKIE_BUTTON_SELECTOR = "#onetrust-accept-btn-handler"


def db_updates(produto, db_conn) -> None:
    if not db_conn:
        raise Exception("Conexão com o banco de dados falhou.")
    if have_product_in_bd(db_conn, produto):
        atual_product = get_product(db_conn, produto)
        if atual_product is not None:
            if atual_product["price"] != produto["price"]:
                update_price(db_conn, produto)
    else:
        insert_product(db_conn, produto)


def fetch_product_data(item) -> dict[str, str]:
    """Fetches product data from the given item element."""
    descricao = item.find_element(By.TAG_NAME, "h3").text.strip()
    preco = item.find_element(By.CLASS_NAME, "priceCard").text.strip()
    link = item.find_element(By.CLASS_NAME, "productLink").get_attribute("href").strip()
    image_element = item.find_element(By.CLASS_NAME, "imageCard")
    image_url = image_element.get_attribute("src")

    return {
        "adm": "kabum",
        "name": descricao,
        "price": preco,
        "link": link,
        "url_image": image_url,
    }


def process_item(item) -> None | dict[str, str]:
    preco = item.find_element(By.CLASS_NAME, "priceCard").text.strip()
    if preco == "R$ ----" or preco == "----" or "x" in preco:
        return
    return fetch_product_data(item)


def process_products(driver) -> None:
    """Iterates over each product on the page and processes its data."""
    print("verificando tabela de produtos no site")
    start_t = datetime.now()

    WebDriverWait(driver, 15, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, TABLE_SELECTOR))
    )
    table = driver.find_elements(By.CSS_SELECTOR, TABLE_SELECTOR)

    print("Iterando página")
    with ThreadPoolExecutor(max_workers=5) as executor:
        produtos = list(executor.map(process_item, table))
    produtos = list(filter(lambda x: x is not None, produtos))

    driver.execute_script("arguments[0].scrollIntoView();", table[-1])
    with get_db_connection() as db_conn:
        for x in produtos:
            db_updates(produto=x, db_conn=db_conn)

    print(f"tempo de leitura de página = {datetime.now() - start_t}")


def handle_pagination(driver):
    """Handles pagination by clicking the 'next' button and processing subsequent pages."""
    try:
        process_products(driver)
        next_element = WebDriverWait(driver, 5, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, NEXT_BUTTON_SELECTOR))
        )
        next_element.click()
        sleep(1)
        handle_pagination(driver)
    except (
        NoSuchElementException,
        ElementNotInteractableException,
        TimeoutException,
    ) as e:
        print(f"Erro na paginação: {e}")
        print("Finalizando o scraping...")
        return


def main_selenium(driver, URL, table_selector):
    """Main function to initialize scraping process."""
    global TABLE_SELECTOR
    TABLE_SELECTOR = table_selector
    print(f"Iniciando Scraping, URL = {URL}")
    driver.get(URL)

    cookie_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, COOKIE_BUTTON_SELECTOR))
    )
    cookie_button.click()

    handle_pagination(driver)
