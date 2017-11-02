import dependency_injector.containers as containers
import dependency_injector.providers as providers
from redis import Redis

from strongr.core.cache import get_cache
from strongr.core.lock.lockfactory import get_lock
import strongr.core

from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base

class Gateways(containers.DeclarativeContainer):
    """IoC container of gateway components."""

    cache = providers.Singleton(get_cache)
    lock = providers.Factory(get_lock)

    redis = providers.Singleton(Redis.from_url, url=strongr.core.Core.config().redis.url)

    sqlalchemy_engine = providers.Singleton(engine_from_config, configuration=strongr.core.Core.config().db.engine.as_dict(), prefix='') # construct engine from config
    sqlalchemy_session = providers.Singleton(sessionmaker(bind=sqlalchemy_engine()))
    sqlalchemy_base = providers.Singleton(declarative_base)
