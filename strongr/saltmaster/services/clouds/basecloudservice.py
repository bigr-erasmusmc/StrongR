from abc import ABCMeta, abstractmethod

from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor


class BaseCloudService():
    __metaclass__ = ABCMeta
    handlers = {}

    def __init__(self):
        self.setup()

    @abstractmethod
    def setup(self):
        return

    def injectHandler(self, handler, command):
        # TODO: do propper type checking
        self.handlers[handler] = command

    def injectHandlers(self, handlers):
        for handler in handlers:
            self.injectHandler(handler, handlers[handler])

    def getCommandBus(self, middlewares=None):
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(self.handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
