from .wrapper import Command

import strongr.core.domain.schedulerdomain

class TestCommand(Command):
    """
    Runs experimental testcode

    test:run
    """
    def handle(self):
        scheduler_service = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService()
        scheduler_queryfactory = strongr.core.domain.schedulerdomain.SchedulerDomain.queryFactory()
        scheduler_querybus = scheduler_service.getQueryBus()

        request_resources_required = scheduler_queryfactory.newRequestResourcesRequired()
        scheduler_querybus.handle(request_resources_required)
