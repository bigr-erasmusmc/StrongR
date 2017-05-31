import filelock

import strongr.core

class DoDelayedTasksHandler:
    def __call__(self, command):
        schedulerService = strongr.core.Core.domains().schedulerDomain().schedulerService()
        queryBus = schedulerService.getQueryBus()
        queryFactory = strongr.core.Core.domains().schedulerDomain().queryFactory()

        commandBus = schedulerService.getCommandBus()
        commandFactory = strongr.core.Core.domains().schedulerDomain().commandFactory()

        tasks = queryBus.handle(queryFactory.newRequestScheduledTasks())

        cache = strongr.core.Core.cache()
        if not cache.exists("tasks.running"):
            cache.set("tasks.running", {}, 3600)

        for t in tasks:
            runningTasks = cache.get("tasks.running")
            taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(t))
            if taskinfo == None: # this should be an exception at some point
                continue
            if taskinfo["taskid"] in runningTasks and runningTasks[taskinfo["taskid"]]:
                continue

            node = queryBus.handle(queryFactory.newFindNodeWithAvailableResources(taskinfo["cores"], taskinfo["ram"]))
            if node == None: # this should be an exception at some point
                continue
            commandBus.handle(commandFactory.newClaimResourcesOnNode(node, taskinfo["cores"], taskinfo["ram"]))
            runningTasks[taskinfo["taskid"]] = True
            cache.set("tasks.running", runningTasks, 3600)
