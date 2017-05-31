from cleo import Application

from strongr.cli import DeploySingleCommand, ListDeployedVmsCommand,\
        RunShellCodeCommand, DeployManyCommand,\
        AddTaskCommand, GetTaskStatusCommand,\
        RunResourceManager

import strongr.core
import json

core = strongr.core.getCore()
coreContainer = core

with open('config.json', 'r') as file:
    config = json.load(file)
    coreContainer.config.update(config)

application = Application()
application.add(DeploySingleCommand(coreContainer))
application.add(ListDeployedVmsCommand(coreContainer))
application.add(RunShellCodeCommand(coreContainer))
application.add(DeployManyCommand(coreContainer))
application.add(AddTaskCommand(coreContainer))
application.add(GetTaskStatusCommand(coreContainer))
application.add(RunResourceManager(coreContainer))


if __name__ == '__main__':
    application.run()
