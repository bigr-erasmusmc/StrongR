from cleo import Application
from cleo.inputs.argv_input import ArgvInput

from strongr.cli import DeploySingleCommand, ListDeployedVmsCommand,\
        RunShellCodeCommand, DeployManyCommand,\
        AddTaskCommand, GetTaskStatusCommand,\
        RunResourceManager, PrintConfig,\
        IsValidUserCommand, RunRestServerCommand,\
        RunCeleryCommand, DestroySingleCommand,\
        DestroyManyCommand

import strongr.core
import logging.config

# Use CLEO ArgvInput to extract some parameters
# this dependency gets injected into
# application.run(..) as well
argvInputs = ArgvInput()

# env is used for loading the right config environment
env = "develop"
if argvInputs.has_parameter_option('env'):
    env = argvInputs.get_parameter_option('env')

core = strongr.core.getCore()

configDomain = core.domains().configDomain()
configDomain.configService().getCommandBus().handle(configDomain.commandFactory().newLoadConfig(env))

logging.config.dictConfig(core.config().logger.as_dict())

application = Application()

application.add(DeploySingleCommand(core))
application.add(ListDeployedVmsCommand(core))
application.add(RunShellCodeCommand(core))
application.add(DeployManyCommand(core))
application.add(AddTaskCommand(core))
application.add(GetTaskStatusCommand(core))
application.add(RunResourceManager(core))
application.add(PrintConfig(core))
application.add(IsValidUserCommand(core))
application.add(RunRestServerCommand(core))
application.add(RunCeleryCommand(core))
application.add(DestroySingleCommand(core))
application.add(DestroyManyCommand(core))


if __name__ == '__main__':
    application.run(input_=argvInputs)
