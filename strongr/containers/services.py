import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.services import CloudServices, CommandFactory

class Services(containers.DeclarativeContainer):
    """IoC container of service providers."""
    cloudServices = providers.Singleton(CloudServices)
    commandFactory = providers.Singleton(CommandFactory)
