import os, logging, copy
from pymongo import MongoClient, UpdateOne
from pymongo.errors import ConnectionFailure

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

_client = None

def get_client():
    global _client

    if _client is not None:
        return _client

    uri = os.getenv("MONGO_URI")
    if not uri:
        logging.error("Variável de ambiente MONGO_URI não encontrada.")
        return None

    try:
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        return _client
    except ConnectionFailure:
        logging.error("Falha ao conectar ao MongoDB Atlas.")
        return None


def get_db():
    client = get_client()
    if not client:
        return None, None

    db_name = os.getenv("MONGO_DB_NAME")
    return client, client[db_name]


def upsert_collection1(data: list[dict]):
    client, db = get_db()
    if not client:
        return

    new_data = copy.deepcopy(data)
    atributos_remover = {"preco", "updated"}

    for item in new_data:
        for attr in atributos_remover:
            item.pop(attr, None)

    collection_name = os.getenv("MONGO_COLLECTION_1")
    collection = db[collection_name]

    collection.create_index("key", unique=True)

    operations = []
    for item in new_data:
        filter_query = {"key": item["key"]}
        operations.append(
            UpdateOne(filter_query, {"$set": item}, upsert=True)
        )

    try:
        if operations:
            result = collection.bulk_write(operations)
            logging.info(
                f"Collection1 - Upserts: {result.upserted_count}, Modificados: {result.modified_count}"
            )
    except Exception as e:
        logging.error(f"Erro no upsert da collection1: {e}")


def insert_collection2(data: list[dict]):
    client, db = get_db()
    if not client:
        return

    new_data = copy.deepcopy(data)
    atributos_remover = {"nome", "plataforma", "loja", "href", "url_imagem"}

    for item in new_data:
        for attr in atributos_remover:
            item.pop(attr, None)

    collection_name = os.getenv("MONGO_COLLECTION_2")
    collection = db[collection_name]

    try:
        if new_data:
            result = collection.insert_many(new_data)
            logging.info(f"Collection2 - Inseridos: {len(result.inserted_ids)}")
    except Exception as e:
        logging.error(f"Erro ao inserir na collection2: {e}")


def read_collection3() -> list[dict]:
    client, db = get_db()
    if not client:
        return []

    collection_name = os.getenv("MONGO_COLLECTION_3")
    collection = db[collection_name]

    try:
        documents = list(collection.find({}, {"_id": 0}))
        return documents
    except Exception as e:
        logging.error(f"Erro ao ler collection3: {e}")
        return []


def upsert_collection3(data: list[dict]):
    client, db = get_db()
    if not client:
        return
    
    new_data = copy.deepcopy(data)
    atributos_remover = {"nome", "plataforma", "loja", "href", "url_imagem"}

    for item in new_data:
        for attr in atributos_remover:
            item.pop(attr, None)

    collection_name = os.getenv("MONGO_COLLECTION_3")
    collection = db[collection_name]

    collection.create_index("key", unique=True)

    operations = []
    for item in new_data:
        filter_query = {"key": item["key"]}
        operations.append(
            UpdateOne(filter_query, {"$set": item}, upsert=True)
        )

    try:
        if operations:
            result = collection.bulk_write(operations)
            logging.info(
                f"Collection3 - Upserts: {result.upserted_count}, Modificados: {result.modified_count}"
            )
    except Exception as e:
        logging.error(f"Erro no upsert da collection3: {e}")
