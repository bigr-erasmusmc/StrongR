from strongr.core.abstracts.abstractservice import AbstractService

from strongr.schedulerdomain.command import ScheduleJob, RunEnqueuedJobs,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartJobOnVm, CheckJobRunning, \
                                            EnsureMinAmountOfNodes, ScaleOut, \
                                            JobFinished, VmCreated,\
                                            VmReady, VmDestroyed, VmNew, CheckScaling,\
                                            CleanupNodes

from strongr.schedulerdomain.handler import ScheduleJobHandler, RunEnqueuedJobsHandler,\
                                            ClaimResourcesOnNodeHandler, ReleaseResourcesOnNodeHandler,\
                                            StartJobOnVmHandler, CheckJobRunningHandler,\
                                            EnsureMinAmountOfNodesHandler, ScaleOutHandler, \
                                            RequestFinishedJobsHandler, JobFinishedHandler,\
                                            VmDestroyedHandler, VmReadyHandler,\
                                            VmCreatedHandler, VmNewHandler, CheckScalingHandler,\
                                            CleanupNodesHandler

from strongr.schedulerdomain.query import RequestScheduledJobs, RequestJobInfo,\
                                            FindNodeWithAvailableResources, RequestFinishedJobs,\
                                            RequestResourcesRequired, RequestVmsByState

from strongr.schedulerdomain.handler import RequestScheduledTasksHandler, RequestTaskInfoHandler,\
                                            FindNodeWithAvailableResourcesHandler, RequestResourcesRequiredHandler,\
                                            RequestVmsByStateHandler

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
                        RunEnqueuedJobsHandler: RunEnqueuedJobs,
                        ClaimResourcesOnNodeHandler: ClaimResourcesOnNode,
                        ReleaseResourcesOnNodeHandler: ReleaseResourcesOnNode,
                        StartJobOnVmHandler: StartJobOnVm,
                        CheckJobRunningHandler: CheckJobRunning,
                        EnsureMinAmountOfNodesHandler: EnsureMinAmountOfNodes,
                        ScaleOutHandler: ScaleOut,
                        JobFinishedHandler: JobFinished,
                        VmCreatedHandler: VmCreated,
                        VmDestroyedHandler: VmDestroyed,
                        VmReadyHandler: VmReady,
                        VmNewHandler: VmNew,
                        CheckScalingHandler: CheckScaling,
                        CleanupNodesHandler: CleanupNodes
                    })
        return self._command_bus

    def getQueryBus(self):
        if self._query_bus is None:
            self._query_bus = self._make_default_querybus({
                    RequestScheduledTasksHandler: RequestScheduledJobs,
                    RequestTaskInfoHandler: RequestJobInfo,
                    FindNodeWithAvailableResourcesHandler: FindNodeWithAvailableResources,
                    RequestFinishedJobsHandler: RequestFinishedJobs,
                    RequestResourcesRequiredHandler: RequestResourcesRequired,
                    RequestVmsByStateHandler: RequestVmsByState
                })
        return self._query_bus
