from cleo import Application

from cli import DeploySingleCommand
from cli import ListDeployedVmsCommand
from cli import RunShellCodeCommand

application = Application()
application.add(DeploySingleCommand())
application.add(ListDeployedVmsCommand())
application.add(RunShellCodeCommand())

if __name__ == '__main__':
    application.run()
