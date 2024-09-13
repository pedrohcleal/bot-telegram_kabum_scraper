from dotenv import load_dotenv
import os, requests

load_dotenv()

# Agora as variáveis estão disponíveis globalmente
print(os.getenv("MY_VARIABLE"))

advertiser_id = os.getenv('17729')
access_token = os.getenv('access_token')

def create_affiliate_link(original_url) -> str:
    url_api = 'https://api.awin.com/publishers/1715259/linkbuilder/generate'
    access_token = '3f27bf47-1470-46e4-9a98-8732316d385c'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "advertiserId": advertiser_id,
        "destinationUrl" : original_url,
        "shorten": True
    }
    
    response = requests.post(url_api, headers=headers, json=data)
    #response = requests.get('https://api.awin.com/accounts', headers=headers)
    
    if response.status_code == 200:
        return response.json[""]
    else:
        return f"Erro: {response.status_code}, {response.content}"

if __name__ == '__main__':
    original_url = 'https://www.kabum.com.br/produto/115413/headset-gamer-redragon-lamia-2-rgb-7-1-40mm-suporte-incluso-h320rgb-1'
    #affiliate_link = create_affiliate_link(access_token, advertiser_id, original_url)
    #print(f'Link de afiliado: {affiliate_link}')