from .wrapper import Command

import uuid

class DeploySingleCommand(Command):
    """
    Deploys a VM in the cloud. A first step towards elasticity.

    deploy:single
    """
    def handle(self):
        cloudServices = self.getDomains().cloudDomain().cloudService()
        commandFactory = self.getDomains().cloudDomain().commandFactory()

        cores = int(self.ask('How many processing cores should the VM have? (default 1): ', 1))
        ram = int(self.ask('How much memory in GiB should the VM have? (default 4): ', 4))
        name = self.ask('What is the name of the VM? (default generated): ', 'worker-' + str(uuid.uuid4()))

        if not (cores > 0 and ram > 0 and len(name) > 0):
            # TODO: put something sensible in here, this is just a placeholder
            self.error('Invalid input')
            return


        deployVmsCommand = commandFactory.newDeployVmsCommand(names=[name], cores=cores, ram=ram)

        cloudProviderName = self.getContainer().config().clouddomain.driver

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Deploying VM {0} cores={1} ram={2}GiB'.format(name, cores, ram))

        commandBus.handle(deployVmsCommand)
