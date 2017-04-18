from cleo import Command

from services import CloudServices
from commands import ListDeployedVms

class ListDeployedVmsCommand:
    """
    Runs shellcode on a VM in the cloud.

    list:deployedvms
    """

    def handle(self):
        cloudServices = CloudServices()
        cloudNames = cloudServices.getCloudNames()
        # for some reason cleo can not handle arrays with 1 el
        if len(cloudNames) > 1:
            cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)
        else:
            cloudProviderName = cloudNames[0]

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()
        listDeployedVms = ListDeployedVms()
        print(commandBus.handle(listDeployedVms))
