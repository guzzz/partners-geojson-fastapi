import os

from redis import Redis
from structlog import get_logger

log = get_logger()

REDIS_EXPIRATION_TIME: int = os.getenv("REDIS_CALCULUS_EXPIRATION_TIME")


class RedisService:

    def __init__(self):
        self.redis_host = "redis-calculus"
        self.redis_port = 6379
        self.redis = self.connect()

    def connect(self):
        try:
            return Redis(host=self.redis_host, port=self.redis_port, db=0)
        except Exception as exc:
            log.error(
                f"Could not connect to Redis with "
                f"REDIS_HOST: {str(self.redis_host)}" 
                f"REDIS_PORT: {str(self.redis_port)}"
            )
            raise exc

    def get_value(self, key):
        log.info(f"[CACHE - calculus] Getting key: {key}")
        return self.redis.get(key)

    def set_value(self, key, value):
        log.info(f"[CACHE - calculus] Setting key: {key}")
        return self.redis.set(key, value, ex=REDIS_EXPIRATION_TIME)

    def delete_value(self, key):
        log.info(f"[CACHE - calculus] Deleting key: {key}")
        self.redis.delete(key)

    def clear(self):
        log.info(f"[CACHE - calculus] Clearing cache")
        self.redis.flushdb()