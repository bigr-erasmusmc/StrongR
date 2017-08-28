from strongr.core.abstracts.abstractservice import AbstractService

from strongr.configdomain.command import LoadConfig
from strongr.configdomain.handler import LoadConfigHandler

class ConfigService(AbstractService):
    _command_bus = None
    _query_bus = None

    def getCommandBus(self):
        if self._command_bus is None:
            self._command_bus = self._make_default_commandbus({
                    LoadConfigHandler: LoadConfig,
                    })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                })
        return self._query_bus
