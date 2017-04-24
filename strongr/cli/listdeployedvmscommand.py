from .wrapper import Command

class ListDeployedVmsCommand(Command):
    """
    List VMs deployed in the cloud.

    deploy:list
    """

    def __init__(self, coreContainer):
        self._coreContainer = coreContainer
        super(ListDeployedVmsCommand, self).__init__()

    def handle(self):
        cloudServices = CloudServices()
        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()
        listDeployedVms = ListDeployedVms()
        print(commandBus.handle(listDeployedVms))
