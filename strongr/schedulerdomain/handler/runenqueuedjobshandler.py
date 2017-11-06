import strongr.core
import strongr.core.domain.schedulerdomain
import strongr.core.gateways

from strongr.schedulerdomain.model import Job, JobState


class RunEnqueuedJobsHandler:
    def __call__(self, command):
        # this command should be simplified at some point
        # finding jobs and a vm to run the job on could be
        # done in one sql query for example.

        SchedulerDomain = strongr.core.domain.schedulerdomain.SchedulerDomain

        schedulerService = SchedulerDomain.schedulerService()
        commandBus = schedulerService.getCommandBus()

        queryBus = schedulerService.getQueryBus()
        queryFactory = SchedulerDomain.queryFactory()

        commandFactory = SchedulerDomain.commandFactory()

        jobs = queryBus.handle(queryFactory.newRequestScheduledJobs()) # this query only gives us JobState enqueued and assigned jobs

        failed_to_find_vm_count = 0
        for job in jobs:
            if failed_to_find_vm_count > 50:
                # if we weren't able to start last 50 jobs give up
                return

            # task is not running, let's try to execute it on an available node
            vm_id = queryBus.handle(queryFactory.newFindNodeWithAvailableResources(job.cores, job.ram))
            if vm_id == None:
                failed_to_find_vm_count += 1
                continue

            commandBus.handle(commandFactory.newStartJobOnVm(vm_id, job.job_id))


        # move scaleout / scalin to separate command
        if coresshort > 0:
            # scaleout
            commandBus.handle(commandFactory.newScaleOut(coresshort, memshort))
        else:
            # scalein
            pass
