from crud import insert_gpu, gpu_have_in_bd, get_gpu, update_gpu_price
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from db_config import get_db_connection
import pprint

def iterar_pag(driver):
    #table_selector = "#listing > div.sc-gsTEea.sc-202cc1e9-2.ezCvIu.SzkqH > div > div > div.sc-hKgJUU.hzqTWi > div > main > *" # Categoria hardware/GPU
    table_selector = "#listing > div.sc-ikPAEB.sc-202cc1e9-2.jcryDv.SzkqH > div > div > div.sc-biBsmb.kcFaol > div > main > *" # Categoria hardware

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, table_selector))
    )
    table = driver.find_elements(By.CSS_SELECTOR, table_selector)
    print('iterando pagina')
    for index, item in enumerate(table):
        descricao = item.find_element(By.TAG_NAME, "h3")
        preco = item.find_element(By.CLASS_NAME, "priceCard")
        link = item.find_element(By.CLASS_NAME, "productLink")
        href_value = link.get_attribute("href")
        image_element = item.find_element(By.CLASS_NAME, "imageCard")
        image_url = url_main + image_element.get_attribute('src')
 
        gpu_item = {}
        gpu_item["adm"] = "kabum"
        gpu_item["name"] = descricao.text.strip()
        gpu_item["price"] = preco.text.strip()
        gpu_item["link"] = href_value.strip()
        gpu_item["url_image"] = image_url

        pprint.pprint(gpu_item)

        with get_db_connection() as db_conn:
            gpu = get_gpu(db_conn, gpu_item)
            if gpu_have_in_bd(db_conn, gpu_item):
                if gpu["price"] != gpu_item["price"]:
                    update_gpu_price(db_conn, gpu_item)
            elif not gpu_have_in_bd(db_conn, gpu_item):
                insert_gpu(db_conn, gpu_item)

        if index == len(table) - 1:
            driver.execute_script("arguments[0].scrollIntoView();", preco)  # scrollar
            sleep(1)


def percorrer_pags(driver):
    iterar_pag(driver)
    try:
        next_element = driver.find_element(
            By.CSS_SELECTOR,
            "#listingPagination > ul > li.next > a",
        )
        next_element.click()
        sleep(3)
    except NoSuchElementException as e:
        print("elemento de click next não encontrado, finalizando...")
        raise e
    except ElementNotInteractableException as e:
        print("elemento de click next não pode ser iterado, finalizando...")
        raise e
    print("Indo para a próxima página")
    percorrer_pags(driver)


def main_selenium(driver, URL):
    global url_main
    url_main = "https://www.kabum.com.br/"
    print("Iniciando Scraping, URL =", URL)
    driver.get(URL)
    sleep(1)
    cookie_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
        )
    )
    cookie_button.click()
    percorrer_pags(driver)
