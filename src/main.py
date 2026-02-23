from scraper.engine import extrair_dados
from utils.helpers import comparar_preco
from database import upsert_collection1, insert_collection2, upsert_collection3, read_collection3
import logging

def storage_data(dados):
    latest_prices = read_collection3()
    products_with_new_prices = comparar_preco(dados, latest_prices)
    upsert_collection1(products_with_new_prices)
    insert_collection2(products_with_new_prices)
    upsert_collection3(products_with_new_prices)


def run():
    logging.info("Iniciando o processo de scraping...")
    
    # 1. Coleta os dados usando o Playwright
    dados = extrair_dados()
    
    # 2. Se houver dados, envia para o MongoDB
    if dados:
      storage_data(dados)
    else:
        logging.warning("Nenhum dado foi coletado para salvar.")

if __name__ == "__main__":
    import time
    inicio = time.time()
    run()
    print(f"Demorou: {round(time.time() - inicio, 2)} segundos")