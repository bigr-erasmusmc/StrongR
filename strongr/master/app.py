from cleo import Application

from cli import DeploySingleCommand
from cli import ListDeployedVmsCommand

application = Application()
application.add(DeploySingleCommand())
application.add(ListDeployedVmsCommand())

if __name__ == '__main__':
    application.run()
