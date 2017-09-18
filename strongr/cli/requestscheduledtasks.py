from .wrapper import Command

class RequestScheduledTasks(Command):
    """
    Shows the task queue.

    task:list
    """
    def handle(self):
        schedulerService = self.getDomains().schedulerDomain().schedulerService()
        queryFactory = self.getDomains().schedulerDomain().schedulerQueryFactory()

        query = commandFactory.newRequestScheduledTasks()
        result = schedulerService.getQueryBus().handle(query)
        print(json.dumps(result))

