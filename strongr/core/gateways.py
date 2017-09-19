import dependency_injector.containers as containers
import dependency_injector.providers as providers
from redis import Redis

from strongr.core.cache import get_cache
import strongr.core


class Gateways(containers.DeclarativeContainer):
    """IoC container of gateway components."""

    cache = providers.Singleton(get_cache)
    redis = providers.Singleton(Redis.from_url, url=strongr.core.Core.config.redis.url)
