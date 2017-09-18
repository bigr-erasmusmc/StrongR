from .wrapper import Command

import json

class GetTaskStatusCommand(Command):
    """
    Get task status. For now this returns json with all the enqueued tasks.

    task:status
    """
    def handle(self):
        schedulerService = self.getDomains().schedulerDomain().schedulerService()
        queryFactory = self.getDomains().schedulerDomain().queryFactory()

        query = queryFactory.newRequestScheduledTasks()
        result = schedulerService.getQueryBus().handle(query)
        print(json.dumps(result))
