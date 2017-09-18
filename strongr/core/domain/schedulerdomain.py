import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.schedulerdomain.service import SchedulerService
from strongr.schedulerdomain.factory import CommandFactory, QueryFactory

class SchedulerDomain(containers.DeclarativeContainer):
    """IoC container of service providers."""
    schedulerService = providers.Singleton(SchedulerService)
    commandFactory = providers.Singleton(CommandFactory)
    queryFactory = providers.Singleton(QueryFactory)
