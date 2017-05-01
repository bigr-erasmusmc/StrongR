from cleo import Application

from strongr.cli import DeploySingleCommand
from strongr.cli import ListDeployedVmsCommand
from strongr.cli import RunShellCodeCommand
from strongr.cli import DeployManyCommand

from strongr.core import Core

coreContainer = Core()

application = Application()
application.add(DeploySingleCommand(coreContainer))
application.add(ListDeployedVmsCommand(coreContainer))
application.add(RunShellCodeCommand(coreContainer))
application.add(DeployManyCommand(coreContainer))

if __name__ == '__main__':
    application.run()
