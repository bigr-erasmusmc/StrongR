from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.authdomain.query import IsValidUser
from strongr.authdomain.handler import IsValidUserHandler

class AuthService:
    def getCommandBus(self, middlewares=None):
        # The authdomain does not have a commandbus
        return None

    def getQueryBus(self, middlewares=None):
        handlers = {
                    IsValidUserHandler: IsValidUser.__name__,
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
