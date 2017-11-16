from .wrapper import Command

import strongr.core.domain.schedulerdomain

import strongr.core.domain.schedulerdomain

class TestCommand(Command):
    """
    Runs experimental testcode

    test:run
    """
    def handle(self):
        command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()
        command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()

        command_bus.handle(command_factory.newScaleOut(32, 128))
