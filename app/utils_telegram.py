import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application
from utils import escape_markdown_v2
from time import sleep
from utils_affiliate import create_affiliate_link

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_ID = os.getenv('ID_GROUP')


async def enviar_mensagem(texto):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=GROUP_ID, text=texto)


async def mensagem_novo_valor_gpu(old_produto, produto):
    print('enviando mensagem pro telegram - Novo produto')
    sleep(3)
    old_name = escape_markdown_v2(old_produto['name'])
    old_price = escape_markdown_v2(old_produto['price'])
    new_price = escape_markdown_v2(produto['price'])
    produto_link = escape_markdown_v2(create_affiliate_link(produto["link"]))
    last_update = escape_markdown_v2(old_produto["last_register_date"])

    text = (
        f"🚀 **Black Friday** 🚀\n\n"
        f"🔄 O valor do item *\"{old_name}\"* foi atualizado\n\n"
        f"📉 Valor antigo: *{old_price}*\n"
        f"📈 Valor novo: *{new_price}*\n\n"
        f"🔍 Mais informações: {produto_link}\n\n"
        f"Última atualização foi em: {last_update}"
        f"🔥 Aproveite as ofertas 🔥"
    )
    
    bot = Bot(token=TOKEN)
    await bot.send_photo(chat_id=GROUP_ID, caption=text, parse_mode='MarkdownV2', photo=gpu["url_image"])


async def novo_produto(produto):
    print('enviando mensagem pro telegram - Atualização de produto')
    sleep(3)
    name = escape_markdown_v2(produto['name'])
    price = escape_markdown_v2(produto['price'])
    link = escape_markdown_v2(create_affiliate_link(produto['link']))
    
    text = (
        f"✨ **Novo Produto em Destaque** ✨\n\n"
        f"🆕 *Produto Adicionado:* *\"{name}\"*\n\n"
        f"💰 *Preço:* *{price}*\n\n"
        f"🔗 *Mais detalhes:* {link}\n\n"
        f"🚀 Não perca essa novidade 🚀"
    )
    
    bot = Bot(token=TOKEN)
    await bot.send_photo(chat_id=GROUP_ID, caption=text, parse_mode='MarkdownV2', photo=produto["url_image"])

async def test_envio_mensagem_grupo():
    app = Application.builder().token(TOKEN).build()
    async with app:
        mensage = 'hello, world!'
        await enviar_mensagem(mensage)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_envio_mensagem_grupo())
