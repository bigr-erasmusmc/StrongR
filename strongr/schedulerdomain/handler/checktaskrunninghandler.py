import strongr.core
import os

class CheckTaskRunningHandler:
    def __call__(self, command):
        core = strongr.core.getCore()

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
        cache.set("tasks.running", running)

        os.remove('/tmp/strongr/' + command.taskid)
