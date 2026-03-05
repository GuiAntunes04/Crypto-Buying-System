from connections.redis_client import get_redis_client

redis_client = get_redis_client()

BLOOM_KEY = "transacoes_filter"

def create_filter():
    try:
        redis_client.execute_command(
            "BF.RESERVE",
            BLOOM_KEY,
            0.01,
            100000
        )
    except:
        pass

def transaction_exists(transaction_id):
    return redis_client.execute_command(
        "BF.EXISTS",
        BLOOM_KEY,
        transaction_id
    )

def add_transaction(transaction_id):
    redis_client.execute_command(
        "BF.ADD",
        BLOOM_KEY,
        transaction_id
    )