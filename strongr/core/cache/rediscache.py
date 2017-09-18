import time

from redis import Redis
import strongr.core
import pickle

class RedisCache:
    _redis = None
    _namespace = None

    def __init__(self):
        self._redis = Redis.from_url(strongr.core.getCore().config().cache.redis.url)
        self._namespace = strongr.core.getCore().config().cache.redis.namespace

    def set(self, key, value, timeout):
        self._redis.psetex(self._namespace + key, timeout, pickle.dumps(value))

    def get(self, key):
        return pickle.loads(self._redis.get(self._namespace + key))

    def delete(self, key):
        self._redis.delete(self._namespace + key)

    def exists(self, key):
        return self._redis.exists(self._namespace + key)

