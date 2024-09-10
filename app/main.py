from main_selenium import main_selenium
from chrome_config import create_driver, reset_driver
import time
from time import sleep
from datetime import datetime

driver = create_driver()

while True:
    print("-----> NOVA ITERAÇÃO WHILE <--------")
    # URL = "https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100&facet_filters=&sort=most_searched" # GPU
    URL = "https://www.kabum.com.br/hardware?page_number=1&page_size=100&facet_filters=&sort=most_searched" # Categoria hardware
    
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    start = time.perf_counter()
    try:
        main_selenium(driver, URL)
    except Exception as e:
        print("Ocorre um erro em main_selenium() (main), reiniciando Script")
        print(e)
        
    end = time.perf_counter()
    driver = reset_driver(driver)    
    exec_time = end - start
    log_message = f"Tempo de execução às {current_time} -> {exec_time:.6f} segundos <-\n"

    with open("execs_logs.txt", mode="a", encoding="utf-8") as file:
        file.write(log_message)
    sleep(1)
    print("-----> FIM DA ITERAÇÃO WHILE <--------\n\n")
