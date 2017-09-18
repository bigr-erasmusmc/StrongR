from .wrapper import Command

class DestroyManyCommand(Command):
    """
    Destroys a list of VMs in the cloud.

    destroy:many
        {machines* : The names of the VMs to be destroyed}
    """
    def handle(self):
        cloudServices = self.getDomains().cloudDomain().cloudService()
        commandFactory = self.getDomains().cloudDomain().commandFactory()

        machines = self.argument('machines')

        destroyVmsCommand = commandFactory.newDestroyVmsCommand(names=machines)

        cloudProviderName = self.getContainer().config().clouddomain.driver

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Destroying VMs {0}'.format(machines))

        commandBus.handle(destroyVmsCommand)
