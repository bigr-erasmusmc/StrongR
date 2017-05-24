import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.schedulerdomain.service import SchedulerService
from strongr.schedulerdomain.factory import CommandFactory

class CloudDomain(containers.DeclarativeContainer):
    """IoC container of service providers."""
    schedulerService = providers.Singleton(CloudServices)
    schedulerCommandFactory = providers.Singleton(CommandFactory)
