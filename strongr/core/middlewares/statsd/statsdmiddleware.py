from cmndr import Middleware
from strongr.core.gateways import Gateways

class StatsMiddleware(Middleware):

    def execute(self, command, next_callable):
        namespace = command.__module__.split('.')[1] + '.' + command.__class__.lower
        stats = Gateways.stats()

        stats.incr(namespace, 1)
        with stats.time(namespace):
            ret = next_callable(command)

        return ret
