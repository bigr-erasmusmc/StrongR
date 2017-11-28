from sqlalchemy import func, and_, or_

from strongr.schedulerdomain.model import Job, JobState, VmState, Vm
from .wrapper import Command

import strongr.core.gateways

class TestCommand(Command):
    """
    Runs experimental testcode

    test:run
    """
    def handle(self):
        command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()
        command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()

        command_bus.handle(command_factory.newScaleIn())
