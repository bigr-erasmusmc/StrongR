from abc import ABCMeta, abstractmethod

from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.core.middlewares.celery.celerymiddleware import CeleryMiddleware
from strongr.core.middlewares.logging.loggingmiddleware import LoggingMiddleware

class AbstractService():
    __metaclass__ = ABCMeta

    def _default_middlewares(self, will_return_values):
        return [
                LoggingMiddleware(),
                CeleryMiddleware(will_return_values)
            ]

    def _make_default_querybus(self, mappings, middlewares=None):
        return self._make_default_bus(mappings, middlewares, True)

    def _make_default_commandbus(self, mappings, middlewares=None):
        return self._make_default_bus(mappings, middlewares, False)

    def _make_default_bus(self, mappings, middlewares, will_return_values):
        handlers = {}
        remotable_mappings = []
        for key in mappings.keys():
            handlers[key] = mappings[key].__name__
            remotable_mappings.append(mappings[key].__module__ + '.' + mappings[key].__name__)

        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            bus = CommandBus(middlewares + self._default_middlewares(will_return_values) + [handler])
        else:
            bus = CommandBus(self._default_middlewares(will_return_values) + [handler])

        # this is needed to get remotable (celery) commands working
        # it takes care of routing celery tasks to the appropriate command bus
        from strongr.core.core import core
        core.commandRouter().append_route(remotable_mappings, bus)

        return bus
