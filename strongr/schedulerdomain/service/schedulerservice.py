from strongr.core.abstracts.abstractservice import AbstractService

from strongr.schedulerdomain.command import ScheduleTask, DoDelayedTasks,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartTaskOnNode, CheckTaskRunning, \
                                            EnsureMinAmountOfNodes, ScaleOut

from strongr.schedulerdomain.handler import ScheduleTaskHandler, DoDelayedTasksHandler,\
                                            ClaimResourcesOnNodeHandler, ReleaseResourcesOnNodeHandler,\
                                            StartTaskOnNodeHandler, CheckTaskRunningHandler,\
                                            EnsureMinAmountOfNodesHandler, ScaleOutHandler

from strongr.schedulerdomain.query import RequestScheduledTasks, RequestTaskInfo,\
                                            FindNodeWithAvailableResources
from strongr.schedulerdomain.handler import RequestScheduledTasksHandler, RequestTaskInfoHandler,\
                                            FindNodeWithAvailableResourcesHandler

class SchedulerService(AbstractService):
    _command_bus = None
    _query_bus = None

    def getCommandBus(self):
        if self._command_bus is None:
            self._command_bus = self._make_default_commandbus({
                        ScheduleTaskHandler: ScheduleTask,
                        DoDelayedTasksHandler: DoDelayedTasks,
                        ClaimResourcesOnNodeHandler: ClaimResourcesOnNode,
                        ReleaseResourcesOnNodeHandler: ReleaseResourcesOnNode,
                        StartTaskOnNodeHandler: StartTaskOnNode,
                        CheckTaskRunningHandler: CheckTaskRunning,
                        EnsureMinAmountOfNodesHandler: EnsureMinAmountOfNodes,
                        ScaleOutHandler: ScaleOut
                    })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                    RequestScheduledTasksHandler: RequestScheduledTasks,
                    RequestTaskInfoHandler: RequestTaskInfo,
                    FindNodeWithAvailableResourcesHandler: FindNodeWithAvailableResources
                })
        return self._query_bus
