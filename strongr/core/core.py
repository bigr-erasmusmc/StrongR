import dependency_injector.containers as containers
import dependency_injector.providers as providers

import logging

from .eventspublisher import EventsPublisher
from strongr.core.middlewares.celery.commandrouter import CommandRouter

class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='root', level=logging.DEBUG)

    inter_domain_events_publisher = providers.Singleton(EventsPublisher)
    command_router = providers.Singleton(CommandRouter)
