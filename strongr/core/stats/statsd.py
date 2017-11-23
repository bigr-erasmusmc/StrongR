import statsd

from strongr.core.stats.abstractstats import AbstractStats

class StatsD(AbstractStats):
    _statsd = None

    def __init__(self, config):
        self._statsd = statsd.StatsClient(config)

    def decr(self, namespace, amount, rate=None):
        self._statsd.decr(namespace, amount, rate)

    def gauge(self, namespace, amount, delta=False):
        self._statsd.gauge(namespace, amount, delta)

    def set(self, namespace, arr):
        self._statsd.set(namespace, arr)

    def time(self, namespace):
        return self._statsd.time(namespace)

    def timing(self, namespace, timems):
        self._statsd.timing(namespace, timems)

    def incr(self, namespace, amount, rate=None):
        self._statsd.incr(namespace, amount, rate)
