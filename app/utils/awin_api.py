from dotenv import load_dotenv
import os, requests
from time import sleep

load_dotenv()

advertiser_id = os.getenv("advertiser_id")
access_token = os.getenv("access_token")
publisher_id = os.getenv("publisher_id")
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}


def create_affiliate_link(original_url) -> str | None:
    sleep(3)
    url_api: str = (
        f"https://api.awin.com/publishers/{publisher_id}/linkbuilder/generate"
    )

    data: dict[str, str] = {
        "advertiserId": advertiser_id,
        "destinationUrl": original_url,
        # "shorten": True,
    }

    response: requests.Response = requests.post(url_api, headers=headers, json=data)
    # response = requests.get('https://api.awin.com/accounts', headers=headers)

    if response.status_code == 200:
        return str(response.json()["url"])  # ["shortUrl"]
    else:
        sleep(120)
        print(f"Erro: {response.status_code}, {response.content}")
        print("Tentando criar link de afiliado novamente")
        create_affiliate_link(original_url)


if __name__ == "__main__":
    original_url = "https://www.kabum.com.br/"
    affiliate_link = create_affiliate_link(original_url=original_url)
    print(f"Link de afiliado: '{affiliate_link}'")
