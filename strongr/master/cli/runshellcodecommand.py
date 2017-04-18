from cleo import Command

from services import CloudServices
from commands import RunShellCode

class RunShellCodeCommand(Command):
    """
    Runs shellcode on a VM in the cloud.

    shell:run
        {--r|remote=? : If set, runs the code on the specified host}
        {cmd* : shellcode to be run on the specified host(s)}
    """

    def handle(self):
        host = self.option('remote')
        cmd = self.argument('cmd')

        if not host:
            host = '*'

        runShellCode = RunShellCode().host(host).sh(cmd)

        cloudServices = CloudServices()
        cloudNames = cloudServices.getCloudNames()
        # for some reason cleo can not handle arrays with 1 el
        if len(cloudNames) > 1:
            cloudProviderName = self.choice('Please select a cloud provider (default {0})'.format(cloudNames[0]), cloudNames, 0)
        else:
            cloudProviderName = cloudNames[0]

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()

        print(commandBus.handle(runShellCode))
