import strongr.core
import os

import strongr.core.domain.schedulerdomain
import strongr.core.domain.clouddomain
from strongr.core.gateways import Gateways


class CheckTaskRunningHandler:
    def __call__(self, command):
        SchedulerDomain = strongr.core.domain.schedulerdomain.SchedulerDomain
        CloudDomain = strongr.core.domain.clouddomain.CloudDomain

        core = strongr.core.getCore()
        cache = Gateways.cache()

        schedulerService = SchedulerDomain.schedulerService()
        commandBus = schedulerService.getCommandBus()
        commandFactory = SchedulerDomain.commandFactory()
        queryBus = schedulerService.getQueryBus()
        queryFactory = SchedulerDomain.queryFactory()

        cloudQueryBus = CloudDomain.cloudService().getCloudServiceByName(core.config().clouddomain.driver).getQueryBus()
        cloudQueryFactory = CloudDomain.queryFactory()

        jid = cache.get("jidmap." + command.taskid)
        status = cloudQueryBus.handle(cloudQueryFactory.newRequestJidStatus(jid))
        if status == None and not status:
            # job not finished yet
            return

        print("Job finished {}".format(command.taskid))
        taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(command.taskid))
        running = cache.get("tasks.running")
        if running is not None and command.taskid in running:
            del running[command.taskid]
            cache.set("tasks.running", running, 3600)

        os.remove('/tmp/strongr/' + command.taskid)

        node = cache.get("tidtonode." + command.taskid)
        if node is not None:
            commandBus.handle(commandFactory.newReleaseResourcesOnNode(node, taskinfo["cores"], taskinfo["ram"]))
