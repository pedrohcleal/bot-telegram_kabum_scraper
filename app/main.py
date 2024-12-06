from selenium.webdriver.chrome.webdriver import WebDriver
from services.kabum_scraper import main_selenium
from config.chrome_config import create_driver
import time
from time import sleep
from datetime import datetime
import json

init = 0
pont = init
max = 5

while True:
    print("-----> NOVA ITERAÇÃO WHILE <--------")

    current_time: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    start: float = time.perf_counter()
    urls: list[dict[str, str]] = json.loads(open("urls.json").read())

    with create_driver() as driver:
        try:
            item: dict[str, str] = urls[pont]
            url: str = item["URL"]
            table_selector: str = item["TABLE_SELECTOR"]
            categoria = item["categoria"]
            main_selenium(driver, url, table_selector, categoria)
        except Exception as e:
            print("Ocorre um erro em main_selenium() (main), reiniciando Script")
            print(e)

    pont += 1
    if pont > max:
        pont = init

    end: float = time.perf_counter()
    exec_time: float = end - start

    print(f"Tempo de execução às {current_time} -> {exec_time:.6f} segundos <-\n")
    print("-----> FIM DA ITERAÇÃO WHILE <--------\n\n")
