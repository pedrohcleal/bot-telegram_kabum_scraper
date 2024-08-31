from main_selenium import main_selenium
from chrome_config import create_driver, reset_driver
import time
from time import sleep
from datetime import datetime

driver = create_driver()

while True:
    print("-----> NOVA ITERAÇÃO WHILE <--------")
    boole = False
    start = time.perf_counter()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        main_selenium(driver)
    except Exception:
        print("Ocorre um erro em main_selenium() (main), reiniciando Script")
        boole = True
    driver = reset_driver(driver)

    end = time.perf_counter()
    exec_time = end - start
    log_message = f"Tempo de execução às {current_time} -> {exec_time:.6f} segundos <- | com erro? -> {boole} \n"

    with open("execs_logs.txt", mode="a", encoding="utf-8") as file:
        file.write(log_message)
    sleep(30)
    print("-----> NOVA ITERAÇÃO WHILE <--------")
