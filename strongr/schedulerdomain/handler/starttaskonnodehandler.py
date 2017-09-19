import strongr
from strongr.core.gateways import Gateways


class StartTaskOnNodeHandler:
    def __call__(self, command):
        core = strongr.core.getCore()
        schedulerService = core.domains().schedulerDomain().schedulerService()
        queryBus = schedulerService.getQueryBus()
        queryFactory = core.domains().schedulerDomain().queryFactory()

        cloudCommandBus = core.domains().cloudDomain().cloudService().getCloudServiceByName(core.config().clouddomain.driver).getCommandBus()
        cloudCommandFactory = core.domains().cloudDomain().commandFactory()

        taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(command.taskid))

        jid = cloudCommandBus.handle(cloudCommandFactory.newRunShellCodeCommand(sh=taskinfo["cmd"], host=command.node))
        cache = Gateways.cache()
        cache.set("jidmap." + taskinfo["taskid"], jid, 3600)
        cache.set('tidtonode.' + taskinfo["taskid"], command.node, 3600)
        cache.delete('clouddomain.jobs.running')
        # invalidate this cache key, else the system might think the job is
        # already finished while in reality it hasn't even started yet
