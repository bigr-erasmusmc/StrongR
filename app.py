from cleo import Application
from cleo.inputs.argv_input import ArgvInput

import strongr.core
import logging.config
from strongr.core.domain.configdomain import ConfigDomain

# Use CLEO ArgvInput to extract some parameters
# this dependency gets injected into
# application.run(..) as well

argvInputs = ArgvInput()

# env is used for loading the right config environment
env = "develop"
if argvInputs.has_parameter_option('env'):
    env = argvInputs.get_parameter_option('env')

core = strongr.core.Core

ConfigDomain.configService().getCommandBus().handle(ConfigDomain.commandFactory().newLoadConfig(env))

logging.config.dictConfig(core.config().logger.as_dict())

from strongr.cli import DeploySingleCommand, ListDeployedVmsCommand,\
        DeployManyCommand,\
        AddJobCommand, GetFinishedJobsCommand,\
        RunResourceManager, PrintConfig,\
        IsValidUserCommand, RunRestServerCommand,\
        RunCeleryCommand, DestroySingleCommand,\
        DestroyManyCommand, EnsureMinAmountOfNodesCommand, \
        MakeDbCommand, RunTestsCommand, TestCommand


application = Application()

application.add(DeploySingleCommand())
application.add(ListDeployedVmsCommand())
application.add(DeployManyCommand())
application.add(AddJobCommand())
application.add(GetFinishedJobsCommand())
application.add(RunResourceManager())
application.add(PrintConfig())
application.add(IsValidUserCommand())
application.add(RunRestServerCommand())
application.add(RunCeleryCommand())
application.add(DestroySingleCommand())
application.add(DestroyManyCommand())
application.add(EnsureMinAmountOfNodesCommand())
application.add(MakeDbCommand())
application.add(RunTestsCommand())
application.add(TestCommand())

if __name__ == '__main__':
    application.run(input_=argvInputs)
