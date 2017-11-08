import strongr.core.domain.clouddomain

class CheckScalingHandler(object):
    def __call__(self, command):
        query_bus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getQueryBus()
        command_bus = strongr.core.domain.clouddomain.CloudDomain().cloudService().getCommandBus()

        query_factory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()
        command_factory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()

        resources_required = query_bus.handle(query_factory.newRequestResourcesRequired())



        if resources_required is None:
            # scalein
            return

        if resources_required['cores'] - 16 > 0: # only scaleout if we are 16 cores or more short
            # scaleout
            command_bus.handle(command_factory.newScaleOut(resources_required['cores'], resources_required['ram']))
