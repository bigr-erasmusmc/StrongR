import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.clouddomain.service import CloudServices
from strongr.clouddomain.factory import CommandFactory, QueryFactory

class CloudDomain(containers.DeclarativeContainer):
    """IoC container of service providers."""
    cloudService = providers.Singleton(CloudServices)
    commandFactory = providers.Singleton(CommandFactory)
    queryFactory = providers.Singleton(QueryFactory)
