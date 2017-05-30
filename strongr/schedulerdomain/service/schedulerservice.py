from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.schedulerdomain.command import ScheduleTask, DoDelayedTasks
from strongr.schedulerdomain.handler import ScheduleTaskHandler, DoDelayedTasksHandler

from strongr.schedulerdomain.query import RequestScheduledTasks
from strongr.schedulerdomain.handler import RequestScheduledTasksHandler
class SchedulerService:
    def getCommandBus(self, middlewares=None):
        handlers = {
                    ScheduleTaskHandler: ScheduleTask.__name__,
                    DoDelayedTasksHandler: DoDelayedTasks.__name__
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])

    def getQueryBus(self, middlewares=None):
        handlers = {
                    RequestScheduledTasksHandler: RequestScheduledTasks.__name__
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
