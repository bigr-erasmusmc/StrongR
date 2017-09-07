from strongr.core.abstracts.abstractservice import AbstractService

from strongr.restdomain.command.oauth2 import AppendGrant, SetToken, BindOauth2ToApp
from strongr.restdomain.handler.oauth2 import AppendGrantHandler, SetTokenHandler, BindOauth2ToAppHandler, \
    RetrieveUserByClientIdHandler

from strongr.restdomain.query.oauth2 import RetrieveClient, RetrieveGrant, \
    RetrieveTokenByAccessToken, RetrieveTokenByRefreshToken, RetrieveUserByClientId
from strongr.restdomain.handler.oauth2 import RetrieveClientHandler, RetrieveGrantHandler,\
                                        RetrieveTokenByAccessTokenHandler, RetrieveTokenByRefreshTokenHandler

class Oauth2Service(AbstractService):
    _command_bus = None
    _query_bus = None

    def getCommandBus(self):
        if self._command_bus is None:
            self._command_bus = self._make_default_commandbus({
                    AppendGrantHandler: AppendGrant,
                    SetTokenHandler: SetToken,
                    BindOauth2ToAppHandler: BindOauth2ToApp
                })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                    RetrieveClientHandler: RetrieveClient,
                    RetrieveGrantHandler: RetrieveGrant,
                    RetrieveTokenByAccessTokenHandler: RetrieveTokenByAccessToken,
                    RetrieveTokenByRefreshTokenHandler: RetrieveTokenByRefreshToken,
                    RetrieveUserByClientIdHandler: RetrieveUserByClientId
                })
        return self._query_bus

    def getSchemas(self):
        from strongr.restdomain.model.oauth2 import Client, Grant, Token, User
        return [Client, Grant, Token, User]

