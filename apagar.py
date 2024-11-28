import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Conectar ao MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["bus_stops"]
collection = db["stops"]

# Função para apagar todas as paradas cadastradas
def apagar_paradas():
    # Apaga todos os documentos da coleção "stops"
    result = collection.delete_many({})  # Remove todos os documentos
    print(f"{result.deleted_count} paradas foram apagadas com sucesso!")

# Apagar todas as paradas
if __name__ == "__main__":
    apagar_paradas()
