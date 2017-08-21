from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.restdomain.query.wsgi import RetrieveBlueprints
from strongr.restdomain.handler.wsgi import RetrieveBlueprintsHandler

class WsgiService:
    def getCommandBus(self, middlewares=None):
        return None # WsgiService has no commandbus yet

    def getQueryBus(self, middlewares=None):
        handlers = {
                    RetrieveBlueprintsHandler: RetrieveBlueprints.__name__
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
