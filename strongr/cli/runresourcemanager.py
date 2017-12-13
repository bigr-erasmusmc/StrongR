from strongr.core.domain.schedulerdomain import SchedulerDomain
from strongr.core.domain.clouddomain import CloudDomain
from .wrapper import Command

import time
import schedule
from celery import Celery
import strongr.core

class RunResourceManager(Command):
    """
    Runs the resource manager. This should be done on your salt master.

    resourcemanager:run
    """
    def handle(self):
        schedulerService = SchedulerDomain.schedulerService()
        commandFactory = SchedulerDomain.commandFactory()

        CloudDomain.cloudService().start_reactor() # enable salt reactor

        command_bus = schedulerService.getCommandBus()
        run_enqueued_jobs_command = commandFactory.newRunEnqueuedJobs()
        check_scaling_command = commandFactory.newCheckScaling()
        cleanup_nodes = commandFactory.newCleanupNodes()
        cleanup_jobs = commandFactory.newCleanupOldJobs()
        log_stats = commandFactory.newLogStats()

        self.info('Running.')

        celery = Celery('strongr', broker=strongr.core.Core.config().celery.broker, backend=strongr.core.Core.config().celery.backend)

        remotable_commands = strongr.core.Core.config().celery.remotable_commands.as_dict()
        for domain in remotable_commands:
            for command in remotable_commands[domain]:
                strongr.core.Core.command_router().enable_route_for_command(celery, '{}.{}'.format(domain, command))

        schedule.every(1).seconds.do(command_bus.handle, run_enqueued_jobs_command)
        schedule.every(5).seconds.do(command_bus.handle, check_scaling_command)
        schedule.every(10).seconds.do(command_bus.handle, log_stats)
        schedule.every(5).minutes.do(command_bus.handle, cleanup_nodes)
        schedule.every(30).minutes.do(command_bus.handle, cleanup_jobs)

        while True:
            schedule.run_pending()
            time.sleep(.5)
