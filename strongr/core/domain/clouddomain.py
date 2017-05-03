import dependency_injector.containers as containers
import dependency_injector.providers as providers

from strongr.clouddomain.service import CloudServices
from strongr.clouddomain.factory import CommandFactory

from strongr.clouddomain.event import NewVmDeployed

class CloudDomain(containers.DeclarativeContainer):
    """IoC container of service providers."""
    cloudServices = providers.Singleton(CloudServices)
    cloudCommandFactory = providers.Singleton(CommandFactory)

    events = providers.Object({\
        "NewVmDeployed": NewVmDeployed \
        })
