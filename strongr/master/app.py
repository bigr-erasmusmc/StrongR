from cleo import Application

from cli import DeploySingleCommand
from cli import ListDeployedVmsCommand
from cli import RunShellCodeCommand
from cli import DeployManyCommand

application = Application()
application.add(DeploySingleCommand())
application.add(ListDeployedVmsCommand())
application.add(RunShellCodeCommand())
application.add(DeployManyCommand())

if __name__ == '__main__':
    application.run()
