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


# Função para cadastrar ou atualizar a parada no MongoDB com coordenadas fornecidas (PUT)
def cadastrar_ou_atualizar_parada(name, lat, lng):
    # Verificar se a parada já existe (por nome)
    parada = {
        "name": name,
        "coordinates": {"lat": lat, "lng": lng}
    }

    # Tentar atualizar a parada existente com base no nome
    result = collection.update_one(
        {"name": name},  # Filtro para encontrar a parada pelo nome
        {"$set": parada},  # Atualiza as coordenadas e o nome
        upsert=True  # Se não encontrar, insere um novo documento
    )

    if result.matched_count > 0:
        print(f"Parada '{name}' atualizada com sucesso!")
    else:
        print(f"Parada '{name}' cadastrada com sucesso!")


# Paradas para cadastrar ou atualizar com as novas coordenadas
paradas = [
    {"name": "Parada Fortaleza Zone 6", "lat": -3.7655206838953506, "lng": -38.567800063041176},
    {"name": "Parada Fortaleza Zone 7", "lat": -3.7651610986131185, "lng": -38.56467211071524},
    {"name": "Parada Fortaleza Zone 8", "lat": -3.766793614622331, "lng": -38.55972072070641},
    {"name": "Parada Fortaleza Zone 9", "lat": -3.769907612402276, "lng": -38.56085946834862},
    {"name": "Parada Fortaleza Zone 10", "lat": -3.7729856408319264, "lng": -38.56813880448394}
]

# Cadastro das paradas
if __name__ == "__main__":
    for parada in paradas:
        cadastrar_ou_atualizar_parada(parada["name"], parada["lat"], parada["lng"])
