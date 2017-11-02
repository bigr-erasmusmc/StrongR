from strongr.core.abstracts.abstractservice import AbstractService

from strongr.schedulerdomain.command import ScheduleJob, DoDelayedTasks,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartJobOnVm, CheckJobRunning, \
                                            EnsureMinAmountOfNodes, ScaleOut, \
                                            JobFinished, VmCreated,\
                                            VmReady, VmDestroyed

from strongr.schedulerdomain.handler import ScheduleJobHandler, DoDelayedTasksHandler,\
                                            ClaimResourcesOnNodeHandler, ReleaseResourcesOnNodeHandler,\
                                            StartJobOnVmHandler, CheckJobRunningHandler,\
                                            EnsureMinAmountOfNodesHandler, ScaleOutHandler, \
                                            RequestFinishedJobsHandler, JobFinishedHandler

from strongr.schedulerdomain.query import RequestScheduledJobs, RequestJobInfo,\
                                            FindNodeWithAvailableResources, RequestFinishedJobs
from strongr.schedulerdomain.handler import RequestScheduledTasksHandler, RequestTaskInfoHandler,\
                                            FindNodeWithAvailableResourcesHandler, VmDestroyedHandler,\
                                            VmReadyHandler, VmCreatedHandler

class SchedulerService(AbstractService):
    _command_bus = None
    _query_bus = None

    def register_models(self):
        import strongr.schedulerdomain.model as model
        # importing alone is enough for registration

    def getCommandBus(self):
        if self._command_bus is None:
            self._command_bus = self._make_default_commandbus({
                        ScheduleJobHandler: ScheduleJob,
                        DoDelayedTasksHandler: DoDelayedTasks,
                        ClaimResourcesOnNodeHandler: ClaimResourcesOnNode,
                        ReleaseResourcesOnNodeHandler: ReleaseResourcesOnNode,
                        StartJobOnVmHandler: StartJobOnVm,
                        CheckJobRunningHandler: CheckJobRunning,
                        EnsureMinAmountOfNodesHandler: EnsureMinAmountOfNodes,
                        ScaleOutHandler: ScaleOut,
                        JobFinishedHandler: JobFinished,
                        VmCreatedHandler: VmCreated,
                        VmDestroyedHandler: VmDestroyed,
                        VmReadyHandler: VmReady
                    })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                    RequestScheduledTasksHandler: RequestScheduledJobs,
                    RequestTaskInfoHandler: RequestJobInfo,
                    FindNodeWithAvailableResourcesHandler: FindNodeWithAvailableResources,
                    RequestFinishedJobsHandler: RequestFinishedJobs
                })
        return self._query_bus
