import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .domain import CloudDomain, SchedulerDomain, ConfigDomain

class Domains(containers.DeclarativeContainer):
    """IoC container of domains."""
    cloudDomain = providers.Factory(CloudDomain)
    schedulerDomain = providers.Factory(SchedulerDomain)
    configDomain = providers.Factory(ConfigDomain)
