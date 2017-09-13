from .wrapper import Command

class ListDeployedVmsCommand(Command):
    """
    List VMs deployed in the cloud.

    deploy:list
    """
    def handle(self):
        cloudService = self.getDomains().cloudDomain().cloudService()
        queryFactory = self.getDomains().cloudDomain().queryFactory()

        cloudProviderName = self.getContainer().config().clouddomain.driver

        cloudService = cloudService.getCloudServiceByName(cloudProviderName)
        queryBus = cloudService.getQueryBus()
        listDeployedVms = queryFactory.newListDeployedVmsCommand()
        print(queryBus.handle(listDeployedVms))
