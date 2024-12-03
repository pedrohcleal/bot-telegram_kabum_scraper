![python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![postgres](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![SQLITE](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![telegram-bot](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)

# 🛒 Kabum Scraper & Telegram Bot

Este projeto realiza o scraping de produtos de diversas categorias do site Kabum (hardware, periféricos, computadores, etc.) e utiliza um bot do Telegram para enviar atualizações rápidas sobre preços e novos produtos diretamente para um grupo.

## 🚀 Funcionalidades

- **Scraping Automático**: Utiliza Selenium para percorrer páginas de produtos da Kabum, coletando informações como nome, preço, link e imagem.
- **Armazenamento no Banco de Dados**: Os dados dos produtos são salvos em um banco PostgreSQL, e novos preços são atualizados conforme necessário. Além disso, o backup é feito em SQLite.
- **Bot do Telegram**: Envia notificações automáticas e rápidas para um grupo do Telegram quando novos produtos são detectados ou preços são atualizados.
- **Configuração Flexível**: As URLs e seletores CSS para scraping são configurados através do arquivo `urls.json`, que contém as categorias e o seletor do elemento `table` para os produtos.
- **Execução Contínua**: O bot é projetado para funcionar continuamente, garantindo que as atualizações ocorram sem interrupções.
- **Geração de Link de Afiliado**: Cria links curtos de afiliado usando a API da Awin, integrados nas mensagens do Telegram.


## 📝 Configuração do Ambiente

Altere o arquivo `.env.example` para `.env` com as seguintes variáveis:

```bash
TELEGRAM_TOKEN=""
ID_GROUP=""
access_token=''
advertiser_id=''
publisher_id=''
host=''
port=''
principaluser=''
senha=''
```

## 🔧 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/pedrohcleal/bot-telegram_kabum_scraper.git
   cd bot-telegram_kabum_scraper_bd
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente criando o arquivo `.env` com seus tokens e IDs.

4. Inicie o scraping e o bot:
   ```bash
   cd app
   python app/main.py
   ```

## 🔗 API da Awin

O projeto usa a API da Awin para gerar links de afiliados. Para mais informações sobre a API, consulte a [documentação oficial](https://wiki.awin.com/index.php/API_Documentation).

A Awin limita o número de solicitações de API a 20 chamadas por minuto por usuário

## ⚠️ Limites da Telegram Bot API:

- Não enviar mais de uma mensagem por segundo para um chat específico.
- Não enviar mais de 30 mensagens por segundo para múltiplos usuários.
- Não enviar mais de 20 mensagens por minuto para o mesmo grupo.

Exceder esses limites pode resultar em erros de "Too Many Requests" (429).

##  Contribuições

Se você gostou do projeto e deseja apoiar o desenvolvimento, sinta-se à vontade para fazer uma contribuição via PIX:

**Chave PIX**: `pedroleal360@gmail.com`

Agradeço seu apoio! Sua contribuição ajuda a manter o projeto ativo e a implementar novas funcionalidades.
