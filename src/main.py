from scraper.engine import extrair_dados # Sua função com Playwright
from database import save_to_mongo
import logging

def run():
    logging.info("Iniciando o processo de scraping...")
    
    # 1. Coleta os dados usando o Playwright
    dados = extrair_dados()
    
    # 2. Se houver dados, envia para o MongoDB
    if dados:
        save_to_mongo(dados)
    else:
        logging.warning("Nenhum dado foi coletado para salvar.")

if __name__ == "__main__":
    run()