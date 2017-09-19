from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import json

class GetTaskStatusCommand(Command):
    """
    Get task status. For now this returns json with all the enqueued tasks.

    task:status
    """
    def handle(self):
        schedulerService = SchedulerDomain.schedulerService()
        queryFactory = SchedulerDomain.queryFactory()

        query = queryFactory.newRequestScheduledTasks()
        result = schedulerService.getQueryBus().handle(query)
        print(json.dumps(result))
