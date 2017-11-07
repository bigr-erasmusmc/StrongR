from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import time
import schedule

class RunResourceManager(Command):
    """
    Runs the resource manager. This should be done on your salt master.

    resourcemanager:run
    """
    def handle(self):
        schedulerService = SchedulerDomain.schedulerService()
        commandFactory = SchedulerDomain.commandFactory()

        commandBus = schedulerService.getCommandBus()
        run_enqueued_jobs_command = commandFactory.newRunEnqueuedJobs()
        check_scaling_command = commandFactory.newCheckScaling()

        self.info('Running.')

        schedule.every(1).seconds.do(commandBus.handle, run_enqueued_jobs_command)
        schedule.every(5).seconds.do(commandBus.handle, check_scaling_command)

        while True:
            schedule.run_pending()
            time.sleep(.5)
