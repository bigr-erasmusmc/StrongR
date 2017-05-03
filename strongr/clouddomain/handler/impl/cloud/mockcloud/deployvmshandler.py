from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmsHandler

from strongr.clouddomain.event import NewVmDeployed

class DeployVmsHandler(AbstractDeployVmsHandler):
    def __call__(self, commands):
        for command in commands:
            newVmDeployedEvent = NewVmDeployed(command.name, command.cores, command.ram)
            self.executeAndPublishDomainEvent(event=newVmDeployedEvent, callable=lambda: None)
