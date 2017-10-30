import strongr.core
import strongr.core.domain.schedulerdomain
import strongr.core.gateways

from strongr.schedulerdomain.model import Job, JobState


class DoDelayedTasksHandler:
    def __call__(self, command):
        SchedulerDomain = strongr.core.domain.schedulerdomain.SchedulerDomain

        schedulerService = SchedulerDomain.schedulerService()
        commandBus = schedulerService.getCommandBus()

        queryBus = schedulerService.getQueryBus()
        queryFactory = SchedulerDomain.queryFactory()

        commandFactory = SchedulerDomain.commandFactory()

        memshort = 0
        coresshort = 0

        jobs = queryBus.handle(queryFactory.newRequestScheduledJobs()) # this query only gives us enqueued, assigned and running jobs

        for job in jobs:
            if job.state == JobState.RUNNING:
                # check if task is running or finished
                commandBus.handle(commandFactory.newCheckJobRunning(job.job_id))
            else:
                # task is not running, let's try to execute it on an available node
                vm_id = queryBus.handle(queryFactory.newFindNodeWithAvailableResources(job.cores, job.ram))
                if vm_id == None:
                    memshort += job.cores
                    coresshort += job.ram
                    continue

                commandBus.handle(commandFactory.newStartJobOnVm(vm_id, job.job_id))

        if coresshort > 0:
            # scaleout
            commandBus.handle(commandFactory.newScaleOut(coresshort, memshort))
        else:
            # scalein
            pass
