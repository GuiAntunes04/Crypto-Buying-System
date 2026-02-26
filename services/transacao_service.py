from datetime import datetime
from connections.database import get_db_client
from services.binance_service import get_preco_atual
from connections.redis_client import get_redis_client
import json

redis_client = get_redis_client()

def get_collection():
    client = get_db_client()
    db = client["crypto_db"]
    return db["transacoes"]

def executar_transacao(usuario_id: str, ticker: str, tipo: str, quantidade: float):

    preco_atual = get_preco_atual(ticker)

    doc = {
        "usuario_id": usuario_id,
        "ticker": ticker,
        "tipo": tipo.lower(),
        "quantidade": quantidade,
        "preco_unitario": preco_atual,
        "timestamp": datetime.utcnow()
    }

    collection = get_collection()
    result = collection.insert_one(doc)

    doc["_id"] = str(result.inserted_id)

    # 🔥 Publica evento no Redis
    redis_client.publish(
        "canal_transacoes",
        json.dumps({
            "usuario_id": usuario_id,
            "ticker": ticker,
            "tipo": tipo,
            "quantidade": quantidade
        })
    )

    return doc