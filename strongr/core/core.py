import logging

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.core.middlewares.celery.commandrouter import CommandRouter
from .cache import Cache
from .domaineventspublisher import DomainEventsPublisher
from .domains import Domains

from sqlalchemy import create_engine


def _make_db_conn():
    engine = create_engine(core.config()['database.uri'], echo=True)
    return engine

class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='strongr')

    domains = providers.Factory(Domains)
    domainEventsPublisher = providers.Singleton(DomainEventsPublisher)

    #keyValueStore = providers.Singleton(InMemoryStore)
    cache = providers.Singleton(Cache)

    #threadPool = ThreadPoolExecutor(max_workers=3)

    commandRouter = providers.Singleton(CommandRouter)

    db = providers.Singleton(_make_db_conn)

core = Core()
