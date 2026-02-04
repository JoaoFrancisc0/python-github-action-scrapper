import logging
from playwright.sync_api import sync_playwright
from scraper.parsers import scrap_lista_produtos

# Configuração de log
logging.basicConfig(level=logging.INFO)

def extrair_dados():
    """Gerencia o ciclo de vida do browser e coordena a extração."""
    dados_finais = []
    
    with sync_playwright() as p:
        logging.info("Iniciando o navegador...")
        # 'headless=True' é obrigatório para o GitHub Actions
        browser = p.chromium.launch(headless=False) 
        
        # O contexto permite simular resoluções de tela e User-Agents
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        try:
            url = "https://www.amazon.com.br/s?k=Playstation&i=videogames&rh=n%3A7791985011%2Cp_n_condition-type%3A13862762011%2Cp_85%3A19171728011%2Cp_36%3A17270950011&s=exact-aware-popularity-rank&dc&__mk_pt_BR=ÅMÅŽÕÑ&crid=124B3UIUBDLPF&qid=1770236390&rnid=17270949011&sprefix=playstatio%2Cvideogames%2C262&xpid=1HiEmcVl4joMT&ref=sr_st_exact-aware-popularity-rank&ds=v1%3AH%2Fiq5emZLKQk2qmNYltSRZxu3Zf3RzofFuxN4p380KY"
            logging.info(f"Navegando para {url}")
            
            # wait_until="networkidle" espera o site parar de carregar scripts
            page.goto(url, timeout=60000)
            
            # Aqui você chama as funções do seu parsers.py
            # Passamos a 'page' para o parser fazer o trabalho sujo
            dados_finais = scrap_lista_produtos(page, 50)
            
            import pandas as pd
            df = pd.DataFrame(dados_finais)
            df.to_excel("produtos.xlsx", index=False)

            logging.info(f"Extração concluída. {len(dados_finais)} itens encontrados.")
            
        except Exception as e:
            logging.error(f"Erro durante a execução do Playwright: {e}")
            # Opcional: tirar um screenshot para debugar no GitHub Actions
            page.screenshot(path="erro_debug.png")
            
        finally:
            browser.close()
            logging.info("Navegador fechado.")
            
    return dados_finais