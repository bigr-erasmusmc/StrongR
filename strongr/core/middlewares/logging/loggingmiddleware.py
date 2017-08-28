from cmndr import Middleware

import strongr.core
import datetime

class LoggingMiddleware(Middleware):
    _logger = None

    def __init__(self):
        if self._logger is None:
            self._logger = strongr.core.getCore().logger()

    def execute(self, command, next_callable):
        #self._logger.debug('{}: {}'.format(time.time(), command.__dict__))
        cmd_dict = command.__dict__
        timestamp = datetime.datetime.now().isoformat()
        print('{}: {} {}'.format(timestamp, command.__module__ + '.' + command.__class__.__name__, (cmd_dict if cmd_dict else '') ))
        ret = next_callable(command)
        return ret
