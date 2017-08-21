from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.restdomain.command.oauth2 import AppendGrant
from strongr.restdomain.handler.oauth2 import AppendGrantHandler

from strongr.restdomain.query.oauth2 import RetrieveClient, RetrieveGrant,\
                                            RetrieveTokenByAccessToken, RetrieveTokenByRefreshToken
from strongr.restdomain.handler.oauth2 import RetrieveClientHandler, RetrieveGrantHandler,\
                                        RetrieveTokenByAccessTokenHandler, RetrieveTokenByRefreshTokenHandler


class Oauth2Service:
    def getCommandBus(self, middlewares=None):
        handlers = {
                    AppendGrantHandler: AppendGrant.__name__,
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])

    def getQueryBus(self, middlewares=None):
        handlers = {
                    RetrieveClientHandler: RetrieveClient.__name__,
                    RetrieveGrantHandler: RetrieveGrant.__name__,
                    RetrieveTokenByAccessTokenHandler: RetrieveTokenByAccessToken.__name__,
                    RetrieveTokenByRefreshTokenHandler: RetrieveTokenByRefreshToken.__name__
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
