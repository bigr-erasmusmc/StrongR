import dependency_injector.containers as containers
import dependency_injector.providers as providers

import logging

#import asyncio
#from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from .domains import Domains

from .domaineventspublisher import DomainEventsPublisher

#from .keyvaluestore import InMemoryStore
from .cache import Cache


from strongr.core.middlewares.celery.commandrouter import CommandRouter

class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='root', level=logging.DEBUG)

    domains = providers.Factory(Domains)
    domainEventsPublisher = providers.Singleton(DomainEventsPublisher)

    #keyValueStore = providers.Singleton(InMemoryStore)
    cache = providers.Singleton(Cache)

    #threadPool = ThreadPoolExecutor(max_workers=3)

    commandRouter = providers.Singleton(CommandRouter)

core = Core()
def getCore():
    return core
