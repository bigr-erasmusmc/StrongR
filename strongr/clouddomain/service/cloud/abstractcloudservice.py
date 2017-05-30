from abc import ABCMeta, abstractmethod

from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmHandler, AbstractDeployVmsHandler, \
                                                        AbstractListDeployedVmsHandler, AbstractRunShellCodeHandler

from strongr.clouddomain.command import DeployVm, DeployVms, RunShellCode
from strongr.clouddomain.query import ListDeployedVms

class AbstractCloudService():
    __metaclass__ = ABCMeta
    _commands = {}
    _queries = {}


    _mappings = {
        AbstractDeployVmHandler: DeployVm.__name__, \
        AbstractListDeployedVmsHandler: ListDeployedVms.__name__, \
        AbstractRunShellCodeHandler: RunShellCode.__name__, \
        AbstractDeployVmsHandler: DeployVms.__name__
    }

    def __init__(self):
        for handler in self.getCommandHandlers():
            command = self._getCommandForHandler(handler)
            self._commands[handler] = command
        for handler in self.getQueryHandlers():
            command = self._getCommandForHandler(handler)
            self._queries[handler] = command


    @abstractmethod
    def getCommandHandlers(self):
        return

    @abstractmethod
    def getQueryHandlers(self):
        pass

    def _getCommandForHandler(self, handler):
        for mappedHandler in self._mappings:
            if issubclass(handler, mappedHandler):
                command = self._mappings[mappedHandler]
                # remove from self._mappings so that a handler with multiple inheritance can work
                del self._mappings[mappedHandler]
                return command
        return None

    def _makeBus(self, handlers, middlewares=None):
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])

    def getCommandBus(self, middlewares=None):
        return self._makeBus(self._commands, middlewares)

    def getQueryBus(self, middlewares=None):
        return self._makeBus(self._queries, middlewares)
