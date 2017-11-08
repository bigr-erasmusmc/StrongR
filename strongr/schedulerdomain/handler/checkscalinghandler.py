import strongr.core.domain.schedulerdomain

class CheckScalingHandler(object):
    def __call__(self, command):
        query_bus = strongr.core.domain.schedulerdomain.schedulerdomain.schedulerService().getQueryBus()
        command_bus = strongr.core.domain.schedulerdomain.schedulerdomain().schedulerService().getCommandBus()

        query_factory = strongr.core.domain.schedulerdomain.schedulerdomain.queryFactory()
        command_factory = strongr.core.domain.schedulerdomain.schedulerdomain.commandFactory()

        resources_required = query_bus.handle(query_factory.newRequestResourcesRequired())



        if resources_required is None:
            # scalein
            return

        if resources_required['cores'] - 16 > 0: # only scaleout if we are 16 cores or more short
            # scaleout
            command_bus.handle(command_factory.newScaleOut(resources_required['cores'], resources_required['ram']))
