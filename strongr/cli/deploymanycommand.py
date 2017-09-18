from .wrapper import Command

import uuid

class DeployManyCommand(Command):
    """
    Deploys VM's in the cloud in a parallel way. A first step towards elasticity.

    deploy:many
    """
    def handle(self):
        cloudServices = self.getDomains().cloudDomain().cloudService()
        commandFactory = self.getDomains().cloudDomain().commandFactory()

        cores = int(self.ask('How many processing cores should the VM\'s have? (default 1): ', 1))
        ram = int(self.ask('How much memory in GiB should the VM\'s have? (default 4): ', 4))
        amount = int(self.ask('How many VM\'s should be deployed? (default 2)', 2))

        if not (cores > 0 and ram > 0 and amount > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return

        deployVmNameList = []
        while amount > 0:
            deployVmNameList.append('worker-' + str(uuid.uuid4()))
            amount -= 1

        deployVms = commandFactory.newDeployVmsCommand(names=deployVmNameList, cores=cores, ram=ram)

        cloudProviderName = self.getContainer().config().clouddomain.driver

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Deploying {0} VM\'s with cores={1} ram={2}GiB'.format(amount, cores, ram))

        commandBus.handle(deployVms)
