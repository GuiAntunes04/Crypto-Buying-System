import redis
import os

def get_redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        username=os.getenv("REDIS_USERNAME"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )

