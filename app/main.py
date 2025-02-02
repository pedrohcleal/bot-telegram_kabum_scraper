from services.kabum_scraper import main_scraping_process
import asyncio
from utils.telegram_api import enviar_mensagem_admins
import time

asyncio.run(enviar_mensagem_admins('Atividades do BOT no grupo Iniciadas'))

try:
    while True:
        print("-----> NOVA ITERAÇÃO WHILE <--------")
        
        categorias = ["hardware", "perifericos", "computadores", "gamer", "celular-smartphone", "tv"]
        
        # Marca o tempo de início da iteração
        start_time = time.time()

        for i in categorias:
            main_scraping_process(i)

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        print(f"Tempo gasto para percorrer todas as categorias: {minutes}m {seconds}s")
        print("-----> FIM DA ITERAÇÃO WHILE <--------\n")
        
except Exception as err:
    asyncio.run(enviar_mensagem_admins(f'erro no bot: {err}, encerrando'))
    raise err
finally:
    asyncio.run(enviar_mensagem_admins('Atividades do bot no grupo encerradas'))
