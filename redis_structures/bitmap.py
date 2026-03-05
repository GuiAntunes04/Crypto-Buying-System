from datetime import datetime
from connections.redis_client import get_redis_client

redis_client = get_redis_client()

def get_today_key():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"usuarios_ativos:{today}"

def user_to_offset(user_id):
    return abs(hash(user_id)) % 1000000

def mark_user_active(user_id):
    key = get_today_key()
    offset = user_to_offset(user_id)
    redis_client.setbit(key, offset, 1)

def count_active_users():
    key = get_today_key()
    return redis_client.bitcount(key)