from chrome_config import driver
from crud import insert_gpu, gpu_have_in_bd, get_gpu_price, update_gpu_price
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from db_config import get_db_connection

def iterar_pag(driver):
    table_selector = "#listing > div.sc-gsTEea.sc-202cc1e9-2.ezCvIu.SzkqH > div > div > div.sc-hKgJUU.hzqTWi > div > main > *"
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, table_selector))
    )
    table = driver.find_elements(By.CSS_SELECTOR, table_selector)
    
    print(f"LEN TABLE ={len(table)}")
    for index, item in enumerate(table):
        descricao = item.find_element(By.TAG_NAME, "h3")
        preco = item.find_element(By.CLASS_NAME, "priceCard")
        link = item.find_element(By.CLASS_NAME, "productLink")
        href_value = link.get_attribute("href")
        
        gpu_item = {}
        gpu_item['adm'] = 'kabum'
        gpu_item['name'] = descricao.text.strip()
        gpu_item['price'] = preco.text.strip()
        gpu_item['link'] = href_value.strip()
        
        print(f"Placa = {descricao.text}")
        print(f"Preço = {preco.text}")
        print(f"Link = {href_value}")
        
        with get_db_connection() as db_conn:
            if gpu_have_in_bd(db_conn, gpu_item) and get_gpu_price(db_conn, gpu_item) != gpu_item['price']:
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
    except NoSuchElementException as err:
        return print(f"elemento de click next não encontrado, erro = {err}")
    print(f"Indo para a próxima página")
    percorrer_pags(driver)


if __name__ == "__main__":
    URL = "https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100&facet_filters=&sort=most_searched"
    print("Iniciando Scraping, URL =", URL)
    try:
        driver.get(URL)
        sleep(1)
        cookie_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
        )
        cookie_button.click()
        percorrer_pags(driver)
    finally:
        driver.quit()
