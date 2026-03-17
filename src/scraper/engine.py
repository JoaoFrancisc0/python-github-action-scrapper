import logging, random
from playwright.sync_api import sync_playwright
from scraper.parsers import scrap_lista_produtos, scrap_lista_produtos_ml

USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.110 Safari/537.36",
    
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

logging.basicConfig(level=logging.INFO)

def extrair_dados(urls):
    dados_finais = []
    url_1, url_2 = urls[0], urls[1]
    
    with sync_playwright() as p:
        logging.info("Iniciando o navegador...")

        # proxy_config = {
        #     "server": "http://0.tcp.sa.ngrok.io:18395", # Atualize com a porta atual do Ngrok
        #     "username": os.getenv("PROXY_USER"),
        #     "password": os.getenv("PROXY_PASS")
        # }

        # browser = p.chromium.launch(headless=True, proxy=proxy_config)

        browser = p.chromium.launch(headless=False)

        user_agent_random = random.choice(USER_AGENTS)

        context = browser.new_context(
            user_agent=user_agent_random
        )
        
        page = context.new_page()
        
        try:
            logging.info(f"Navegando para {url_1}")
            page.goto(url_1, timeout=60000)
            dados_amazon = scrap_lista_produtos(page)
            logging.info(f"Extração amazon concluída. {len(dados_amazon)} itens encontrados.")

            logging.info(f"Navegando para {url_2}")
            page.goto(url_2, timeout=60000)
            dados_ml = scrap_lista_produtos_ml(page)
            logging.info(f"Extração mercado livre concluída. {len(dados_ml)} itens encontrados.")
            
            dados_finais = dados_amazon + dados_ml

            logging.info(f"Extração concluída. {len(dados_finais)} itens encontrados.")
            
        except Exception as e:
            logging.error(f"Erro durante a execução do Playwright: {e}")
            page.screenshot(path="erro_debug.png")
            
        finally:
            browser.close()
            logging.info("Navegador fechado.")
            
    return dados_finais