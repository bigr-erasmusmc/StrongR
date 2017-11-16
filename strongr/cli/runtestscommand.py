from .wrapper import Command

import unittest

import strongr.core.domain.schedulerdomain

class RunTestsCommand(Command):
    """
    Runs the unit tests

    unittests:run
    """
    def handle(self):
        command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()
        command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()

        command_bus.handle(command_factory.newScaleOut(32, 128))

        #testsuite = unittest.TestLoader().discover('.')
        #unittest.TextTestRunner(verbosity=1).run(testsuite)
