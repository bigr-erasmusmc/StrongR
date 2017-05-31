import time

class Cache:
    _cache = {}
    _timeout = {}

    def _checkKey(self, key):
        print(self._cache)
        if key in self._timeout and int(time.time()) > self._timeout[key]:
            del self._cache[key]
            del self._timeout[key]


    def set(self, key, value, timeout):
        self._cache[key] = value
        self._timeout[key] = int(time.time()) + timeout

    def get(self, key):
        self._checkKey(key)
        if key in self._cache:
            return self._cache[key]
        return None

    def exists(self, key):
        self._checkKey(key)
        if key in self._cache:
            return True
        return False

