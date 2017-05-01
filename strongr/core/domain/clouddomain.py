import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.cloudDomain.service import CloudServices
from strongr.cloudDomain.factory import CommandFactory

class CloudDomain(containers.DeclarativeContainer):
    """IoC container of service providers."""
    cloudServices = providers.Singleton(CloudServices)
    cloudCommandFactory = providers.Singleton(CommandFactory)
