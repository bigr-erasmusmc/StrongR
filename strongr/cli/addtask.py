from .wrapper import Command

import uuid

class AddTaskCommand(Command):
    """
    Add a task to the resource manager

    task:add
        {--s|cmd: shellcode to be run}
        {--c|cores: the amount of cores necessary to complete the job}
        {--m|ram: the amount of ram necessary to complete the job}
    """
    def handle(self):
        schedulerService = self.getDomains().schedulerDomain().schedulerService()
        commandFactory = self.getDomains().schedulerDomain().schedulerCommandFactory()

        cmd = self.option('cmd')
        cores = int(self.option('cores'))
        ram = int(self.option('ram'))

        if not (cores > 0 and ram > 0 and len(cmd) > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return

        command = commandFactory.newScheduleTaskCommand(uuid.uuid4(), cmd, cores, ram)
        schedulerService.getCommandBus().handle(command)

