from .wrapper import Command

class RunShellCodeCommand(Command):
    """
    Runs shellcode on a VM in the cloud.

    shell:run
        {--r|remote=? : If set, runs the code on the specified host}
        {cmd* : shellcode to be run on the specified host(s)}
    """
    def handle(self):
        services = self.getServicesContainer()
        cloudServices = services.cloudServices()
        commandFactory = services.cloudCommandFactory()

        host = self.option('remote')
        cmd = self.argument('cmd')

        if not host:
            host = '*'

        runShellCode = commandFactory.newRunShellCodeCommand(host=host, sh=cmd)

        cloudNames = cloudServices.getCloudNames()
        cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        commandBus.handle(runShellCode)
