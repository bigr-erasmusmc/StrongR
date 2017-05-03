from .wrapper import Command

import uuid

class DeployManyCommand(Command):
    """
    Deploys VM's in the cloud in a parallel way. A first step towards elasticity.

    deploy:many
    """
    def handle(self):
        services = self.getServicesContainer()
        cloudServices = services.cloudServices()
        commandFactory = services.cloudCommandFactory()

        cores = int(self.ask('How many processing cores should the VM\'s have? (default 1): ', 1))
        ram = int(self.ask('How much memory in GiB should the VM\'s have? (default 4): ', 4))
        amount = int(self.ask('How many VM\'s should be deployed? (default 2)', 2))

        if not (cores > 0 and ram > 0 and amount > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return

        deployVmList = []
        while amount > 0:
            deployVmCommand = commandFactory.newDeployVmCommand(name=str(uuid.uuid4()), cores=cores, ram=ram)
            deployVmList.append(deployVmCommand)
            amount -= 1
        deployVms = commandFactory.newDeployVmsCommand(deployVmList)

        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Deploying {0} VM\'s with cores={1} ram={2}GiB'.format(len(deployVms), cores, ram))

        commandBus.handle(deployVms)
