from .wrapper import Command

class ListDeployedVmsCommand(Command):
    """
    List VMs deployed in the cloud.

    deploy:list
    """
    def handle(self):
        cloudService = self.getDomains().cloudDomain().cloudService()
        queryFactory = self.getDomains().cloudDomain().queryFactory()

        cloudNames = cloudService.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudService.getCloudServiceByName(cloudProviderName)
        queryBus = cloudService.getQueryBus()
        listDeployedVms = queryFactory.newListDeployedVmsCommand()
        print(queryBus.handle(listDeployedVms))
