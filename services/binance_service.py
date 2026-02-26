import requests
from connections.redis_client import get_redis_client

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

redis_client = get_redis_client()

def get_preco_atual(ticker: str):

    symbol = f"{ticker}USDT"
    cache_key = f"preco:{symbol}"

    # 🔹 1. Verifica se já está no cache
    preco_cache = redis_client.get(cache_key)

    if preco_cache:
        return float(preco_cache)

    # 🔹 2. Busca na Binance
    response = requests.get(BINANCE_URL, params={"symbol": symbol})

    if response.status_code != 200:
        raise Exception("Erro ao buscar preço na Binance")

    preco = float(response.json()["price"])

    # 🔹 3. Salva no Redis por 15 segundos
    redis_client.setex(cache_key, 15, preco)

    return preco