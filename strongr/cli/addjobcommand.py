from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import uuid
import base64
import json
import time

class AddJobCommand(Command):
    """
    Add a task to the resource manager

    job:add
        {image : Docker image to be used}
        {script : Shellcode to be executed in docker image, base64 encoded}
        {scratch : Does the docker image use a scratch mount?}
        {cores : The amount of cores needed for execution}
        {memory : The amount of memory in GiB needed for execution}
    """
    def handle(self):
        schedulerService = SchedulerDomain.schedulerService()
        commandFactory = SchedulerDomain.commandFactory()

        image = str(self.argument('image'))
        script = str(base64.b64decode(self.argument('script'))).splitlines()
        job_id = str(int(time.time())) + '-' + str(uuid.uuid4())
        scratch = self._castToBool(self.argument('scratch'))
        cores = int(self.argument('cores'))
        memory = int(self.argument('memory'))

        command = commandFactory.newScheduleJobCommand(image=image, script=script, job_id=job_id, scratch=scratch, cores=cores, memory=memory)
        schedulerService.getCommandBus().handle(command)
        print(json.dumps({'job_id': job_id}))
