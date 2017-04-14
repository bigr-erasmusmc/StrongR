from cleo import Application

#from cli import ConfigHelperCommand
#from cli import OpenNebulaConfigHelper
from cli import DeployOpenNebulaCommand

application = Application()
#application.add(ConfigHelperCommand(application))
#application.add(OpenNebulaConfigHelper())
application.add(DeployOpenNebulaCommand())

if __name__ == '__main__':
    application.run()
