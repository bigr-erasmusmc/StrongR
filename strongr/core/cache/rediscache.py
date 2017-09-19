import pickle
import strongr.core
import strongr.core.gateways
from strongr.core.lock.redislock import RedisLock


class RedisCache:
    _redis = None
    _namespace = None

    def __init__(self):
        self._redis = strongr.core.gateways.Gateways.redis()
        self._namespace = strongr.core.Core.config().cache.redis.namespace

    def set(self, key, value, timeout):
        with RedisLock(key):
            self._redis.delete(self._namespace + key)
            self._redis.setex(self._namespace + key, pickle.dumps(value), timeout)

    def get(self, key):
        with RedisLock(key):
            ret = self._redis.get(self._namespace + key)
        return None if ret is None else pickle.loads(ret)

    def delete(self, key):
        with RedisLock(key):
            self._redis.delete(self._namespace + key)

    def exists(self, key):
        with RedisLock(key):
            return self._redis.exists(self._namespace + key)

