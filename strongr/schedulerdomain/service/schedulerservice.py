from cmndr import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import LazyLoadingInMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from strongr.schedulerdomain.command import ScheduleTask, DoDelayedTasks,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartTaskOnNode
from strongr.schedulerdomain.handler import ScheduleTaskHandler, DoDelayedTasksHandler,\
                                            ClaimResourcesOnNodeHandler, ReleaseResourcesOnNodeHandler,\
                                            StartTaskOnNodeHandler

from strongr.schedulerdomain.query import RequestScheduledTasks, RequestTaskInfo,\
                                            FindNodeWithAvailableResources
from strongr.schedulerdomain.handler import RequestScheduledTasksHandler, RequestTaskInfoHandler,\
                                            FindNodeWithAvailableResourcesHandler
class SchedulerService:
    def getCommandBus(self, middlewares=None):
        handlers = {
                    ScheduleTaskHandler: ScheduleTask.__name__,
                    DoDelayedTasksHandler: DoDelayedTasks.__name__,
                    ClaimResourcesOnNodeHandler: ClaimResourcesOnNode.__name__,
                    ReleaseResourcesOnNodeHandler: ReleaseResourcesOnNode.__name__,
                    StartTaskOnNodeHandler: StartTaskOnNode.__name__
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
                    RequestScheduledTasksHandler: RequestScheduledTasks.__name__,
                    RequestTaskInfoHandler: RequestTaskInfo.__name__,
                    FindNodeWithAvailableResourcesHandler: FindNodeWithAvailableResources.__name__
                }
        extractor = ClassNameExtractor()
        locator = LazyLoadingInMemoryLocator(handlers)
        inflector = CallableInflector()
        handler = CommandHandler(extractor, locator, inflector)
        if middlewares != None:
            return CommandBus(middlewares + [handler])
        return CommandBus([handler])
