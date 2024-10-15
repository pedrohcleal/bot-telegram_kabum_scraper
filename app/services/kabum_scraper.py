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

URL_MAIN = "https://www.kabum.com.br/"
NEXT_BUTTON_SELECTOR = "#listingPagination > ul > li.next > a"
COOKIE_BUTTON_SELECTOR = "#onetrust-accept-btn-handler"


def db_updates(gpu_item):
    with get_db_connection() as db_conn:
        if not db_conn:
            raise Exception("Conexão com o banco de dados falhou.")
        if have_product_in_bd(db_conn, gpu_item):
            atual_product = get_product(db_conn, gpu_item)
            if atual_product is not None:
                if atual_product["price"] != gpu_item["price"]:
                    update_price(db_conn, gpu_item)
        else:
            insert_product(db_conn, gpu_item)


def fetch_product_data(item):
    """Fetches product data from the given item element."""
    descricao = item.find_element(By.TAG_NAME, "h3").text.strip()
    preco = item.find_element(By.CLASS_NAME, "priceCard").text.strip()
    link = item.find_element(By.CLASS_NAME, "productLink").get_attribute("href").strip()
    image_element = item.find_element(By.CLASS_NAME, "imageCard")
    image_url = URL_MAIN + image_element.get_attribute("src")

    return {
        "adm": "kabum",
        "name": descricao,
        "price": preco,
        "link": link,
        "url_image": image_url,
    }


def process_products(driver):
    """Iterates over each product on the page and processes its data."""
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, TABLE_SELECTOR))
    )
    table = driver.find_elements(By.CSS_SELECTOR, TABLE_SELECTOR)
    print("Iterando página")

    for index, item in enumerate(table):
        preco = item.find_element(By.CLASS_NAME, "priceCard").text.strip()
        if preco == "R$ ----" or preco == "----" or "x" in preco:
            continue

        gpu_item = fetch_product_data(item)
        db_updates(gpu_item=gpu_item)
        if index == len(table) - 1:
            driver.execute_script("arguments[0].scrollIntoView();", item)
            sleep(2.5)


def handle_pagination(driver):
    """Handles pagination by clicking the 'next' button and processing subsequent pages."""
    try:
        next_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, NEXT_BUTTON_SELECTOR))
        )
        driver.execute_script("arguments[0].click();", next_element)
        sleep(2)
        process_products(driver)
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
    sleep(1)

    cookie_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, COOKIE_BUTTON_SELECTOR))
    )
    cookie_button.click()

    process_products(driver)
    handle_pagination(driver)
