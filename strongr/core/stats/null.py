from strongr.core.stats.abstractstats import AbstractStats


class NullContextManager:
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass


class Null(AbstractStats):
    def decr(self, namespace, amount, rate=None):
        pass

    def gauge(self, namespace, amount, delta=False):
        pass

    def set(self, namespace, arr):
        pass

    def time(self, namespace):
        return NullContextManager()

    def timing(self, namespace, timems):
        pass

    def incr(self, namespace, amount, rate=None):
        pass
