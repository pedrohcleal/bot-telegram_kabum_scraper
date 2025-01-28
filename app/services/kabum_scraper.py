from database.crud import insert_product, have_product_in_bd, get_product, update_price
from time import sleep
from config.db_config import get_db_connection
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.sanitize import normalize_title_to_link
from utils.telegram_api import enviar_mensagem_admins
import asyncio
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "X-Origin": "Brasil"
}

def update_product_in_db(product, db_conn) -> None:
    if have_product_in_bd(db_conn, product):
        existing_product = get_product(db_conn, product)
        if existing_product and existing_product["price"] != product["price"]:
            update_price(db_conn, product)
    else:
        insert_product(db_conn, product)


def parse_product_data(response_json_data, category) -> list[dict]:
    return [
        {
            "id": x["id"],
            "name": x["attributes"]["title"],
            "price_without_discount": x["attributes"]["price"],
            "price": x["attributes"]["price_with_discount"],
            "quantity_available": x["attributes"]
            .get("offer", {})
            .get("quantity_available", 0)
            if x["attributes"].get("offer") else 0,
            "score_of_ratings": x["attributes"]["score_of_ratings"],
            "number_of_ratings": x["attributes"]["number_of_ratings"],
            "photos_list": x["attributes"]["photos"],#[G][0]
            "url_image": str(x["attributes"]["photos"]["p"][0]),
            "warranty": x["attributes"]["warranty"],
            'categoria': category,
            'link': f'https://www.kabum.com.br/produto/{x["id"]}/{normalize_title_to_link(x["attributes"]["title"])}',
        }
        for x in response_json_data
    ]


def fetch_products_from_api(page: int, category: str) -> list[dict]:
    print('acessando pag ', page)
    url = f"https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/{category}?page_number={page}&page_size=100&facet_filters=&sort=most_searched&is_prime=false&payload_data=products_category_filters&include=gift"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Request error: URL {url}, status_code: {response.status_code}")
        raise err

    return parse_product_data(response.json()['data'], category)


def fetch_all_products(category) -> list[dict]:
    url = f"https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/{category}?page_number=1&page_size=100&facet_filters=&sort=most_searched&is_prime=false&payload_data=products_category_filters&include=gift"
    response = requests.get(url, headers=HEADERS)
    total_pages = response.json()["meta"]["total_pages_count"]
    all_products = []

    print(f'Total pages: {total_pages}')
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(fetch_products_from_api, page, category) for page in range(1, total_pages + 1)
        ]
        for future in futures:
            all_products.extend(future.result())
    
    # for page in range(1, total_pages + 1):
    #     all_products.extend(fetch_products_from_api(page, category))

    print(f"Total time for requests -> {datetime.now() - start_time}")
    return all_products


def process_and_update_products(products) -> None:
    print("Verifying products in the database")
    start_time = datetime.now()

    with get_db_connection() as db_conn:
        for product in products:
            update_product_in_db(product, db_conn)

    print(f"Time to check database = {datetime.now() - start_time}")


def main_scraping_process(category):
    print(f'processing {category}')
    
    products = fetch_all_products(category)
    process_and_update_products(products)
    
    print('--------/----------')
