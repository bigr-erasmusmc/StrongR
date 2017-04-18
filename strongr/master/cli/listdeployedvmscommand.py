from .wrapper import Command

from services import CloudServices
from commands import ListDeployedVms

class ListDeployedVmsCommand(Command):
    """
    List VMs deployed in the cloud.

    deploy:list
    """

    def handle(self):
        cloudServices = CloudServices()
        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()
        listDeployedVms = ListDeployedVms()
        print(commandBus.handle(listDeployedVms))
