import strongr.core

class CheckTaskRunning():
    def __call__(self, command):
        core = strongr.core.getCore()

        cloudQueryBus = core.domains().cloudDomain().cloudService().getCloudServiceByName(core.config.cloud.driver()).getQueryBus()
        cloudQueryFactory = core.domains().cloudDomain().queryFactory()

        jid = core.cache().get("jidmap." + command.taskid)
        status = cloudCommandBus.handle(cloudCommandFactory.newRunShellCodeCommand(sh=taskinfo["cmd"], host=command.node))
