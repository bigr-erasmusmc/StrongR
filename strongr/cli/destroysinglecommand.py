from .wrapper import Command

class DestroySingleCommand(Command):
    """
    Destroys a VM in the cloud.

    deploy:destroy
        {machine : The name of the VM to be destroyed}
    """
    def handle(self):
        cloudServices = self.getDomains().cloudDomain().cloudService()
        commandFactory = self.getDomains().cloudDomain().commandFactory()

        machine = self.argument('machine')
        destroyVmCommand = commandFactory.newDestroyVmCommand(name=machine)

        cloudProviderName = self.getContainer().config().clouddomain.driver

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        self.info('Destroying VM {0}'.format(machine))

        commandBus.handle(destroyVmCommand)
