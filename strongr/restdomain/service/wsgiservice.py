from strongr.core.abstracts.abstractservice import AbstractService

from strongr.restdomain.query.wsgi import RetrieveBlueprints
from strongr.restdomain.handler.wsgi import RetrieveBlueprintsHandler

class WsgiService(AbstractService):
    _command_bus = None
    _query_bus = None

    def getCommandBus(self):
        if self._command_bus is None:
            self._command_bus = self._make_default_commandbus({
                    })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                    RetrieveBlueprintsHandler: RetrieveBlueprints
                })
        return self._query_bus
