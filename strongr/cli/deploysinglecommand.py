from .wrapper import Command

import uuid

class DeploySingleCommand(Command):
    """
    Deploys a VM in the cloud. A first step towards elasticity.

    deploy:single
    """
    def handle(self):
        services = self.getServicesContainer()
        cloudServices = services.cloudServices()
        commandFactory = services.commandFactory()

        cores = int(self.ask('How many processing cores should the VM have? (default 1): ', 1))
        ram = int(self.ask('How much memory in GiB should the VM have? (default 4): ', 4))
        name = self.ask('What is the name of the VM? (default generated): ', str(uuid.uuid4()))

        if not (cores > 0 and ram > 0 and len(name) > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return


        deployVmCommand = commandFactory.newDeployVmCommand(name=name, cores=cores, ram=ram)

        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Deploying VM {0} cores={1} ram={2}GiB'.format(name, cores, ram))

        print(commandBus.handle(deployVmCommand))
