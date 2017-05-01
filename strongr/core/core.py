import dependency_injector.containers as containers
import dependency_injector.providers as providers

import logging

from .domains import Domains

class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='strongr-master')

    domains = providers.Factory(Domains)