from .wrapper import Command

import uuid
import base64
import json
import time

class AddTaskCommand(Command):
    """
    Add a task to the resource manager

    task:add
        {shell : Shellcode to execute}
        {cores : Amount of cores required for the task}
        {mem : Amount of ram in GiB required for the task}
    """
    def handle(self):
        schedulerService = self.getDomains().schedulerDomain().schedulerService()
        commandFactory = self.getDomains().schedulerDomain().commandFactory()

        cmd = str(base64.b64decode(self.argument('shell')))
        cores = int(self.argument('cores'))
        ram = int(self.argument('mem'))

        if not (cores > 0 and ram > 0 and len(cmd) > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return

        taskid = str(int(time.time())) + '-' + str(uuid.uuid4())
        command = commandFactory.newScheduleTaskCommand(taskid, cmd, cores, ram)
        schedulerService.getCommandBus().handle(command)
        print(json.dumps({'taskid': taskid}))
