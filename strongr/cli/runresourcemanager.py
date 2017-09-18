from .wrapper import Command

import time

class RunResourceManager(Command):
    """
    Runs the resource manager. This should be done on your salt master.

    resourcemanager:run
    """
    def handle(self):
        schedulerService = self.getDomains().schedulerDomain().schedulerService()
        commandFactory = self.getDomains().schedulerDomain().commandFactory()

        commandBus = schedulerService.getCommandBus()
        doDelayedTasksCommand = commandFactory.newDoDelayedTasks()

        self.info('Running.')
        while True:
            commandBus.handle(doDelayedTasksCommand)
            time.sleep(1)

