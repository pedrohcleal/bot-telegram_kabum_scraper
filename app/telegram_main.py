import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application
from utils import escape_markdown_v2
from time import sleep
# Carregar variáveis de ambiente
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_ID = os.getenv('ID_GROUP')


async def enviar_mensagem(texto):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=GROUP_ID, text=texto)


async def mensagem_novo_valor_gpu(old_gpu, gpu):
    sleep(3)
    old_name = escape_markdown_v2(old_gpu['name'])
    old_price = escape_markdown_v2(old_gpu['price'])
    new_price = escape_markdown_v2(gpu['price'])
    gpu_link = escape_markdown_v2(gpu["link"])

    text = (
        f"🚀 **Black Friday** 🚀\n\n"
        f"🔄 O valor do item *\"{old_name}\"* foi atualizado\n\n"
        f"📉 Valor antigo: *{old_price}*\n"
        f"📈 Valor novo: *{new_price}*\n\n"
        f"🔍 Mais informações: {gpu_link}\n\n"
        f"🔥 Aproveite as ofertas 🔥"
    )
    
    bot = Bot(token=TOKEN)
    await bot.send_photo(chat_id=GROUP_ID, caption=text, parse_mode='MarkdownV2', photo=gpu["url_image"])


async def novo_produto(gpu):
    sleep(3)
    name = escape_markdown_v2(gpu['name'])
    price = escape_markdown_v2(gpu['price'])
    link = escape_markdown_v2(gpu['link'])
    
    text = (
        f"✨ **Novo Produto em Destaque** ✨\n\n"
        f"🆕 *Produto Adicionado:* *\"{name}\"*\n\n"
        f"💰 *Preço:* *{price}*\n\n"
        f"🔗 *Mais detalhes:* {link}\n\n"
        f"🚀 Não perca essa novidade 🚀"
    )
    
    bot = Bot(token=TOKEN)
    await bot.send_photo(chat_id=GROUP_ID, caption=text, parse_mode='MarkdownV2', photo=gpu["url_image"])
##
async def main():
    app = Application.builder().token(TOKEN).build()
    async with app:
        mensage = 'hello, world!'
        await enviar_mensagem(mensage)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
