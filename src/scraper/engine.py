import logging
import pandas as pd
import os
from playwright.sync_api import sync_playwright
from scraper.parsers import scrap_lista_produtos, scrap_lista_produtos_ml

logging.basicConfig(level=logging.INFO)

def extrair_dados():
    dados_finais = []
    
    with sync_playwright() as p:
        logging.info("Iniciando o navegador...")

        proxy_config = {
            "server": os.getenv("PROXY_SERVER"), # Atualize com a porta atual do Ngrok
            "username": os.getenv("PROXY_USER"),
            "password": os.getenv("PROXY_PASS")
        }

        browser = p.chromium.launch(headless=True, proxy=proxy_config)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        url_amazon = "https://www.amazon.com.br/s?k=Playstation&i=videogames&rh=n%3A7791985011%2Cp_n_condition-type%3A13862762011%2Cp_85%3A19171728011%2Cp_36%3A17270950011&s=exact-aware-popularity-rank&dc&__mk_pt_BR=ÅMÅŽÕÑ&crid=124B3UIUBDLPF&qid=1770236390&rnid=17270949011&sprefix=playstatio%2Cvideogames%2C262&xpid=1HiEmcVl4joMT&ref=sr_st_exact-aware-popularity-rank&ds=v1%3AH%2Fiq5emZLKQk2qmNYltSRZxu3Zf3RzofFuxN4p380KY"
        url_ml = "https://lista.mercadolivre.com.br/games/video-games/novo/playstation_CustoFrete_Gratis_PriceRange_0BRL-500BRL_BestSellers_YES_NoIndex_True?sb=category#applied_filter_id%3Dprice%26applied_filter_name%3DPreço%26applied_filter_order%3D15%26applied_value_id%3D*-500%26applied_value_name%3DBRL*-BRL500%26applied_value_order%3D4%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue"

        try:
            logging.info(f"Navegando para {url_amazon}")
            page.goto(url_amazon, timeout=60000)
            dados_amazon = scrap_lista_produtos(page, 51)
            logging.info(f"Extração amazon concluída. {len(dados_amazon)} itens encontrados.")

            logging.info(f"Navegando para {url_ml}")
            page.goto(url_ml, timeout=60000)
            dados_ml = scrap_lista_produtos_ml(page, 100)
            logging.info(f"Extração mercado livre concluída. {len(dados_ml)} itens encontrados.")
            
            dados_finais = dados_amazon + dados_ml

            df = pd.DataFrame(dados_finais)
            df.to_excel("produtos.xlsx", index=False)

            logging.info(f"Extração concluída. {len(dados_finais)} itens encontrados.")
            
        except Exception as e:
            logging.error(f"Erro durante a execução do Playwright: {e}")
            page.screenshot(path="erro_debug.png")
            
        finally:
            browser.close()
            logging.info("Navegador fechado.")
            
    return dados_finais