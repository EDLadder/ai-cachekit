import redis

class RedisBackend:
    def __init__(self, host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def get(self, key):
        result = self.r.get(key)
        return result.decode() if result else None

    def set(self, key, value):
        self.r.set(key, value)
