import time
import strongr.core.gateways

class RedisLock(object):
    _redis_namespace = 'strongr-redislock-'

    def __init__(self, name, timeout=10):
        self._timeout = timeout
        self._name = name
        self._redis = strongr.core.gateways.Gateways.redis()

    def __enter__(self):
        timeout_after = int(time.time()) + self._timeout
        while not self._redis.setnx(self._redis_namespace + self._name, True) and int(time.time()) > timeout_after:
            time.sleep(.5)
        else:
            return self

        raise IOError('Could not aquire lock for {}'.format(self._name))

    def __exit__(self, type, value, traceback):
        self._redis.delete(self._redis_namespace + self._name)
