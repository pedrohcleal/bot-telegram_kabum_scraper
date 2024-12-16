from services.kabum_scraper import main_selenium
from config.chrome_config import create_driver
import time
from datetime import datetime
import json

init = 0
pont = init
max = 5
start: float = time.perf_counter()
print(datetime.now())

while True:
    print("-----> NOVA ITERAÇÃO WHILE <--------")

    
    
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
        end: float = time.perf_counter()
        exec_time: float = end - start

        print(f"Tempo de execução às -> {exec_time:.6f} segundos <-\n")
        start: float = time.perf_counter()
        pont = init
    
    print("-----> FIM DA ITERAÇÃO WHILE <--------\n\n")
