from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import uuid
import base64
import json
import time

class AddJobCommand(Command):
    """
    Add a task to the resource manager

    task:add
        {shell : Shellcode to execute}
        {cores : Amount of cores required for the task}
        {mem : Amount of ram in GiB required for the task}
    """
    def handle(self):
        schedulerService = SchedulerDomain.schedulerService()
        commandFactory = SchedulerDomain.commandFactory()

        cmd = str(base64.b64decode(self.argument('shell')))
        cores = int(self.argument('cores'))
        ram = int(self.argument('mem'))

        job_id = str(int(time.time())) + '-' + str(uuid.uuid4())
        command = commandFactory.newScheduleJobCommand(job_id, cmd, cores, ram)
        schedulerService.getCommandBus().handle(command)
        print(json.dumps({'job_id': job_id}))
