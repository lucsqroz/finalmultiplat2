import os
import math
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Chave secreta para JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretkey')  # Use uma chave secreta em produção
jwt = JWTManager(app)

# Conectar ao MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["bus_stops"]
collection = db["stops"]

# Função para calcular a distância entre dois pontos usando a fórmula de Haversine
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Função para converter ObjectId em string
def json_serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

# Função para gerar o token JWT automaticamente ao inicializar a aplicação
def generate_token():
    # Simulando login automático, você pode modificar para usar autenticação real se necessário
    access_token = create_access_token(identity="admin", expires_delta=timedelta(hours=1))
    return access_token

# Rota de login (para demonstrar o processo de autenticação)
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "admin" or password != "admin":
        return jsonify({"msg": "Credenciais inválidas"}), 401  # Retorna erro se as credenciais forem incorretas

    # Criação do token JWT válido por 1 hora
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify(access_token=access_token)

# Rota para buscar todas as paradas (requere JWT)
@app.route("/api/all-stops", methods=["GET"])
@jwt_required()
def get_all_stops():
    stops = list(collection.find())
    for stop in stops:
        stop["_id"] = json_serialize(stop["_id"])  # Serializar o ObjectId
    return jsonify(stops)

@app.route("/")
def index():
    # Gerar o token JWT automaticamente ao carregar a página
    access_token = generate_token()
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return render_template('index.html', GOOGLE_MAPS_API_KEY=google_maps_api_key, JWT_TOKEN=access_token)

if __name__ == "__main__":
    app.run(debug=True)
