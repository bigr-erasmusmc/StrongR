from .wrapper import Command

class ListDeployedVmsCommand(Command):
    """
    List VMs deployed in the cloud.

    deploy:list
    """
    def handle(self):
        services = self.getServicesContainer()
        cloudServices = services.cloudServices()
        commandFactory = services.cloudCommandFactory()

        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()
        listDeployedVms = commandFactory.newListDeployedVmsCommand()
        print(commandBus.handle(listDeployedVms))