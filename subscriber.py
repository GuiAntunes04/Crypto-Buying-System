from connections.redis_client import get_redis_client
from redis_structures.bitmap import mark_user_active
from redis_structures.bloomfilter import transaction_exists, add_transaction

import json

redis_client = get_redis_client()

if __name__ == "__main__":

    pubsub = redis_client.pubsub()
    pubsub.subscribe("canal_transacoes")

    print("🔔 Aguardando novas transações...")

    for message in pubsub.listen():

        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])
        except Exception:
            print("❌ Erro ao decodificar mensagem")
            continue

        print("📢 Nova transação recebida:")
        print(data)

        user_id = data.get("usuario_id")
        transaction_id = data.get("transacao_id")

        if not user_id or not transaction_id:
            print("⚠️ Dados incompletos recebidos")
            continue

        # =========================
        # BLOOM FILTER (duplicação)
        # =========================
        if transaction_exists(transaction_id):
            print("⚠️ Transação possivelmente duplicada:", transaction_id)
            continue

        add_transaction(transaction_id)

        # =========================
        # BITMAP (usuário transacionou hoje)
        # =========================
        mark_user_active(user_id)

        print("✅ Estruturas Redis atualizadas")