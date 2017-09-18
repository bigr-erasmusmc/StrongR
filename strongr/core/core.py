import dependency_injector.containers as containers
import dependency_injector.providers as providers

import logging

from strongr.core.cache import get_cache
from .domains import Domains

from .domaineventspublisher import DomainEventsPublisher


from strongr.core.middlewares.celery.commandrouter import CommandRouter

class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='root', level=logging.DEBUG)

    domains = providers.Factory(Domains)
    domainEventsPublisher = providers.Singleton(DomainEventsPublisher)

    cache = providers.Singleton(get_cache)

    commandRouter = providers.Singleton(CommandRouter)

core = Core()
def getCore():
    return core
