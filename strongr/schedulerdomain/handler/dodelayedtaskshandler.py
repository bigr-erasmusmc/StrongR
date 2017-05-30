import filelock

import strongr.core

class DoDelayedTasksHandler:
    def __call__(self, command):
        schedulerService = strongr.core.Core.domains().schedulerDomain().schedulerService()
        queryBus = schedulerService.getQueryBus()
        queryFactory = strongr.core.Core.domains().schedulerDomain().queryFactory()

        tasks = queryBus.handle(queryFactory.newRequestScheduledTasks())

        for t in tasks:
            taskinfo = queryBus.handle(queryFactory.newRequestTaskInfo(t))
            if taskinfo == None: # this should be an exception at some point
                continue


