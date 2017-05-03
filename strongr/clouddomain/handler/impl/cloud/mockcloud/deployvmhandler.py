from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmHandler

from strongr.clouddomain.event import NewVmDeployed

class DeployVmHandler(AbstractDeployVmHandler):
    def __call__(self, command):
        newVmDeployedEvent = NewVmDeployed(command.name, command.cores, command.ram)
        self.executeAndPublishDomainEvent(event=newVmDeployedEvent, callable=lambda: None)
