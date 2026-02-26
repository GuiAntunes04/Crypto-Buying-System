from connections.redis_client import get_redis_client
import json

redis_client = get_redis_client()
if __name__ == "__main__":
    pubsub = redis_client.pubsub()
    pubsub.subscribe("canal_transacoes")

    print("🔔 Aguardando novas transações...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print("📢 Nova transação recebida:")
            print(data)