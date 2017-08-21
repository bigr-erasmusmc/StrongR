import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.restdomain.service import Oauth2Service, WsgiService
from strongr.restdomain.factory.oauth2 import CommandFactory as Oauth2CommandFactory,\
                                                QueryFactory as Oauth2QueryFactory

from strongr.restdomain.factory.wsgi import QueryFactory as WsgiQueryFactory

class RestDomain(containers.DeclarativeContainer):
    """IoC container"""
    oauth2CommandFactory = providers.Singleton(Oauth2CommandFactory)
    oauth2QueryFactory = providers.Singleton(Oauth2QueryFactory)
    oauth2Service = providers.Singleton(Oauth2Service)

    wsgiQueryFactory = providers.Singleton(WsgiQueryFactory)
    wsgiService = providers.Singleton(WsgiService)
