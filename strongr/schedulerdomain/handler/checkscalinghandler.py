import strongr.core.domain.schedulerdomain

class CheckScalingHandler(object):
    def __call__(self, command):
        return # turn off for now since scaleout / scalein is not updated to sqlalchemy yet

        query_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getQueryBus()
        command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()

        query_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.queryFactory()
        command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()

        resources_required = query_bus.handle(query_factory.newRequestResourcesRequired())



        if resources_required is None:
            # scalein
            return

        if resources_required['cores'] - 16 > 0: # only scaleout if we are 16 cores or more short
            # scaleout
            command_bus.handle(command_factory.newScaleOut(resources_required['cores'], resources_required['ram']))
