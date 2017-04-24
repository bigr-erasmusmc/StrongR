from abc import ABCMeta, abstractmethod

from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.domain.commandhandlers.abstract.cloud import AbstractDeployVmHandler, AbstractDeployVmsHandler, \
                                                        AbstractListDeployedVmsHandler, AbstractRunShellCodeHandler
from strongr.domain.commands import DeployVm, DeployVms, ListDeployedVms, RunShellCode


class AbstractCloudService():
    __metaclass__ = ABCMeta
    handlers = {}


    _mappings = {
        AbstractDeployVmHandler: DeployVm.__name__, \
        AbstractListDeployedVmsHandler: ListDeployedVms.__name__, \
        AbstractRunShellCodeHandler: RunShellCode.__name__, \
        AbstractDeployVmsHandler: DeployVms.__name__
    }

    def __init__(self):
        self.setup()

    @abstractmethod
    def setup(self):
        return

    def _getCommandForHandler(self, handler):
        for mappedHandler in self._mappings:
            if issubclass(handler, mappedHandler):
                command = self._mappings[mappedHandler]
                # remove from self._mappings so that a with multiple inheritance can work
                del self._mappings[mappedHandler]
                return command
        return None

    def injectHandler(self, handler):
        command = self._getCommandForHandler(handler)
        if command is not None:
            self.handlers[handler] = command

    def injectHandlers(self, handlers):
        for handler in handlers:
            self.injectHandler(handler)

    def getCommandBus(self, middlewares=None):
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(self.handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
