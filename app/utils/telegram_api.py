import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application
from utils.sanitize import escape_markdown_v2
from time import sleep
from utils.awin_api import create_affiliate_link
from database.crud_prices_hist import get_last_5prices
from config.db_config import get_db_connection
from telegram.error import RetryAfter

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = os.getenv("ID_GROUP")


async def enviar_mensagem(texto):
    bot = Bot(token=TOKEN)
    success = False
    while not success:
        try:
            await bot.send_message(chat_id=GROUP_ID, text=texto)
            success = True
        except RetryAfter as e:
            wait_time = int(e.retry_after)
            print(f"Limite de envio excedido. Aguardando {wait_time} segundos.")
            sleep(wait_time)


async def mensagem_novo_valor_produto(old_produto, produto):
    print("enviando mensagem pro telegram - Atualização de produto")
    sleep(6)
    old_name: str = escape_markdown_v2(old_produto["name"])
    old_price: str = escape_markdown_v2(old_produto["price"])
    new_price: str = escape_markdown_v2(produto["price"])
    produto_link: str = escape_markdown_v2(create_affiliate_link(produto["link"]))
    # last_update: str = escape_markdown_v2(old_produto["last_register_date"])
    with get_db_connection() as conn:
        last_5prices: str = escape_markdown_v2(get_last_5prices(conn, produto))

    text: str = (
        f"🚀 **Black Friday** 🚀\n\n"
        f'🔄 O valor do item *"{old_name}"* foi atualizado\n\n'
        f"📈 Valor antigo: *{old_price}*\n"
        f"📉 Valor novo: *{new_price}*\n\n"
        f"🔍 Mais informações: [Site Kabum]({produto_link})\n\n"
        # f"Última atualização foi em: {last_update}\n\n"
        f"Últimos preços: {last_5prices}\n\n"
        f"🔥 Aproveite as ofertas 🔥"
    )

    bot = Bot(token=TOKEN)
    success = False
    while not success:
        try:
            await bot.send_photo(
                chat_id=GROUP_ID,
                caption=text,
                parse_mode="MarkdownV2",
                photo=produto["url_image"],
            )
            success = True
        except RetryAfter as e:
            wait_time = int(e.retry_after)
            print(f"Limite de envio excedido. Aguardando {wait_time} segundos.")
            sleep(wait_time)


async def novo_produto(produto):
    print("enviando mensagem pro telegram - Novo produto")
    sleep(6)
    name: str = escape_markdown_v2(produto["name"])
    price: str = escape_markdown_v2(produto["price"])
    link: str = escape_markdown_v2(create_affiliate_link(produto["link"]))
    with get_db_connection() as conn:
        last_5prices = escape_markdown_v2(get_last_5prices(conn, produto))

    text = (
        f"✨ **Novo Produto em Destaque** ✨\n\n"
        f'🆕 *Produto Adicionado:* *"{name}"*\n\n'
        f"💰 *Preço:* *{price}*\n\n"
        f"🔗 *Mais detalhes:* [Site Kabum]({link})\n\n"
        f"Últimos preços: {last_5prices}\n\n"
        f"🚀 Não perca essa novidade 🚀"
    )

    bot = Bot(token=TOKEN)
    success = False
    while not success:
        try:
            await bot.send_photo(
                chat_id=GROUP_ID,
                caption=text,
                parse_mode="MarkdownV2",
                photo=produto["url_image"],
            )
            success = True
        except RetryAfter as e:
            wait_time = int(e.retry_after)
            print(f"Limite de envio excedido. Aguardando {wait_time} segundos.")
            sleep(wait_time)


async def test_envio_mensagem_grupo():
    app = Application.builder().token(TOKEN).build()
    async with app:
        mensage = "TESTE ENVIO DE MENSAGEM OK"
        await enviar_mensagem(mensage)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_envio_mensagem_grupo())
