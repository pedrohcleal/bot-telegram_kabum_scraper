# 🛒 Kabum Scraper & Telegram Bot

Este projeto faz o scraping de produtos da categoria de hardware (ex: GPUs) do site Kabum e utiliza um bot do Telegram para enviar atualizações de preço e novos produtos para um grupo. Além disso, gera links de afiliado automaticamente utilizando a API da Awin.

## 🚀 Funcionalidades

- **Scraping Automático**: Utiliza Selenium para percorrer as páginas de produtos da Kabum, coletando informações como nome, preço, link e imagem.
- **Armazenamento no Banco de Dados**: Os dados dos produtos são salvos em um banco PostgreSQL, e novos preços são atualizados conforme necessário.
- **Bot do Telegram**: Envia notificações automáticas para um grupo do Telegram quando novos produtos são detectados ou preços são atualizados.
- **Geração de Link de Afiliado**: Cria links curtos de afiliado usando a API da Awin, integrados nas mensagens do Telegram.
- **Logs de Execução**: Mantém um log de execução detalhado para monitoramento e debug.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python
- **Web Scraping**: `Selenium`, `BeautifulSoup`
- **Banco de Dados**: `PostgreSQL`
- **Bot do Telegram**: `python-telegram-bot`
- **Geração de Link de Afiliado**: `Awin API`
- **Controle de Ambiente**: `dotenv` para carregar variáveis de ambiente

## 📦 Estrutura de Pastas

```bash
├── app
│   ├── config
│   │   ├── chrome_config.py
│   │   └── db_config.py
│   ├── database
│   │   ├── crud.py
│   │   └── crud_prices_hist.py
│   ├── main.py
│   ├── services
│   │   ├── kabum_scraper.py
│   │   └── verificar_banco_main.py
│   ├── urls.json
│   └── utils
│       ├── awin_api.py
│       ├── sanitize.py
│       └── telegram_api.py
├── backups
│   └── kabum.db
├── commands.txt
├── readme.md
├── requirements.txt
└── tests
    ├── tests_bd.py
    ├── tests_others.py
    └── tests_scraper.py
```

## 📝 Configuração do Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```bash
TELEGRAM_TOKEN=seu_token_telegram
ID_GROUP=seu_id_grupo
advertiser_id=seu_advertiser_id
access_token=seu_access_token_awin
publisher_id=seu_publisher_id
```

## 🔧 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_projeto.git
   cd seu_projeto
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente criando o arquivo `.env` com seus tokens e IDs.

4. Inicie o scraping e o bot:
   ```bash
   python bot.py
   ```

## 🔗 API da Awin

O projeto usa a API da Awin para gerar links de afiliados. Para mais informações sobre a API, consulte a [documentação oficial](https://wiki.awin.com/index.php/API_Documentation).

## 📝 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
