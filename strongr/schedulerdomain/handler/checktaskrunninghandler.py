import strongr.core
import os

class CheckTaskRunningHandler:
    def __call__(self, command):
        core = strongr.core.getCore()

        schedulerService = core.domains().schedulerDomain().schedulerService()
        commandBus = schedulerService.getCommandBus()
        commandFactory = core.domains().schedulerDomain().commandFactory()
        queryBus = schedulerService.getQueryBus()
        queryFactory = core.domains().schedulerDomain().queryFactory()

        cloudQueryBus = core.domains().cloudDomain().cloudService().getCloudServiceByName(core.config.cloud.driver()).getQueryBus()
        cloudQueryFactory = core.domains().cloudDomain().queryFactory()

        jid = core.cache().get("jidmap." + command.taskid)
        status = cloudQueryBus.handle(cloudQueryFactory.newRequestJidStatus(jid))
        if status == None and not status:
            # job not finished yet
            return

        cache = core.cache()
        running = cache.get("tasks.running")
        del running[command.taskid]
        cache.set("tasks.running", running, 3600)

        os.remove('/tmp/strongr/' + command.taskid)

        taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(command.taskid))
        commandBus.handle(commandFactory.newReleaseResourcesOnNode(node, taskinfo["cores"], taskinfo["ram"]))
