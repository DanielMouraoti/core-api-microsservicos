from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import redis
import pika
import json

app = FastAPI(title="Core API - Fase 1")

# --- CONEXÕES DE INFRAESTRUTURA ---
# No mundo real, isso ficaria em variáveis de ambiente (.env)
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["core_database"]
users_collection = db["users"]

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# --- MODELOS DE DADOS ---
class User(BaseModel):
    id: str
    name: str
    role: str

class LogMessage(BaseModel):
    service: str
    message: str

# --- ROTAS DA API ---

@app.post("/users", status_code=201)
def create_user(user: User):
    """Salva um usuário no banco de dados MongoDB"""
    user_dict = user.dict()
    # Verifica se já existe
    if users_collection.find_one({"id": user.id}):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    users_collection.insert_one(user_dict)
    return {"message": "Usuário criado com sucesso", "user": user.name}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    """Busca um usuário (com estratégia de Cache no Redis)"""
    # 1. Tenta buscar no Redis primeiro (Super rápido)
    cached_user = redis_client.get(f"user:{user_id}")
    if cached_user:
        return {"source": "REDIS_CACHE", "data": json.loads(cached_user)}

    # 2. Se não achar no cache, vai no MongoDB (Mais lento)
    user = users_collection.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 3. Salva no Redis para as próximas buscas (TTL de 60 segundos)
    redis_client.setex(f"user:{user_id}", 60, json.dumps(user))
    
    return {"source": "MONGODB", "data": user}

@app.post("/logs")
def send_log(log: LogMessage):
    """Publica uma mensagem em uma fila assíncrona no RabbitMQ"""
    try:
        # Conecta no RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        
        # Garante que a fila existe
        channel.queue_declare(queue='logs_queue')
        
        # Envia a mensagem
        message_body = json.dumps(log.dict())
        channel.basic_publish(exchange='', routing_key='logs_queue', body=message_body)
        connection.close()
        
        return {"status": "Log enfileirado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão com mensageria: {str(e)}")
