import strongr.core

class DoDelayedTasksHandler:
    def __call__(self, command):
        core = strongr.core.getCore()
        schedulerService = core.domains().schedulerDomain().schedulerService()

        queryBus = schedulerService.getQueryBus()
        queryFactory = core.domains().schedulerDomain().queryFactory()

        commandBus = schedulerService.getCommandBus()
        commandFactory = core.domains().schedulerDomain().commandFactory()

        tasks = queryBus.handle(queryFactory.newRequestScheduledTasks())

        cache = core.cache()
        if not cache.exists("tasks.running"):
            cache.set("tasks.running", {}, 3600)

        for t in tasks:
            runningTasks = cache.get("tasks.running")
            taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(t))
            if taskinfo == None: # this should be an exception at some point
                continue
            if taskinfo["taskid"] in runningTasks and runningTasks[taskinfo["taskid"]]:
                # check if task is running or finished
                commandBus.handle(commandFactory.newCheckTaskRunning(taskinfo["taskid"]))
            else:
                # task is not running or finished, let's try to execute it on an available node
                node = queryBus.handle(queryFactory.newFindNodeWithAvailableResources(taskinfo["cores"], taskinfo["ram"]))
                if node == None: # this should be an exception at some point
                    # Work in a FIFO-style fashion for the moment. We do not wish to execute the next task even if there
                    # might be enough resources in the cluster for this would not be FIFO.
                    return
                commandBus.handle(commandFactory.newClaimResourcesOnNode(node, taskinfo["cores"], taskinfo["ram"]))
                commandBus.handle(commandFactory.newStartTaskOnNode(node, taskinfo["taskid"]))
                runningTasks[taskinfo["taskid"]] = True
                cache.set("tasks.running", runningTasks, 3600)
