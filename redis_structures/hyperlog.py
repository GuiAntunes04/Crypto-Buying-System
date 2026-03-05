from datetime import datetime
from connections.redis_client import get_redis_client

redis_client = get_redis_client()

def get_today_key():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"usuarios_unicos:{today}"

def add_user(user_id):
    key = get_today_key()
    redis_client.pfadd(key, user_id)

def count_unique_users():
    key = get_today_key()
    return redis_client.pfcount(key)