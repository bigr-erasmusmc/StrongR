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
        self._redis.setex(self._namespace + key, pickle.dumps(value), timeout)

    def get(self, key):
        ret = self._redis.get(self._namespace + key)
        return None if ret is None else pickle.loads(ret)

    def delete(self, key):
        self._redis.delete(self._namespace + key)

    def exists(self, key):
        return self._redis.exists(self._namespace + key)

