import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuração básica de logs para o console do GitHub Actions
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_client():
    """Cria e retorna o cliente do MongoDB Atlas."""
    uri = os.getenv("MONGO_URI")
    if not uri:
        logging.error("Variável de ambiente MONGO_URI não encontrada.")
        return None
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping') # Testa a conexão
        return client
    except ConnectionFailure:
        logging.error("Falha ao conectar ao MongoDB Atlas.")
        return None

def save_to_mongo(data):
    """Função principal para salvar os dados coletados."""
    client = get_client()
    if not client:
        return

    db_name = os.getenv("MONGO_DB_NAME", "meu_scraper")
    coll_name = os.getenv("MONGO_COLLECTION", "dados_coletados")
    
    db = client[db_name]
    collection = db[coll_name]

    try:
        if isinstance(data, list) and data:
            result = collection.insert_many(data)
            logging.info(f"Sucesso: {len(result.inserted_ids)} itens salvos.")
        elif isinstance(data, dict):
            result = collection.insert_one(data)
            logging.info(f"Sucesso: Item salvo com ID {result.inserted_id}.")
    except Exception as e:
        logging.error(f"Erro ao inserir no banco: {e}")
    finally:
        client.close()
        logging.info("Conexão com o banco encerrada.")