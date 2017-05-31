import strongr

class StartTaskOnNodeHandler:
    def __call__(self, command):
        core = strongr.core.getCore()
        schedulerService = core.domains().schedulerDomain().schedulerService()
        queryBus = schedulerService.getQueryBus()
        queryFactory = core.domains().schedulerDomain().queryFactory()

        cloudCommandBus = core.domains().cloudDomain().cloudService().getCloudServiceByName(core.config.cloud.driver()).getCommandBus()
        cloudCommandFactory = core.domains().cloudDomain().commandFactory()

        taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(command.taskid))

        jid = cloudCommandBus.handle(cloudCommandFactory.newRunShellCodeCommand(sh=taskinfo["cmd"], host=command.node))
        core.cache().set("jidmap." + taskinfo["taskid"], jid, 3600)
