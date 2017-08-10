from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.configdomain.command import LoadConfig
from strongr.configdomain.handler import LoadConfigHandler

class ConfigService:
    def getCommandBus(self, middlewares=None):
        handlers = {
                    LoadConfigHandler: LoadConfig.__name__,
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])

    def getQueryBus(self, middlewares=None):
        # The configdomain does not have a querybus
        return None
