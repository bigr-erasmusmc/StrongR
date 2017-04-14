from cleo import Command
from services import CloudServices
from commands import DeployVm

import uuid

class DeployCommand(Command):
    """
    Deploys VM's in the cloud. A first step towards elasticity.

    deploy:opennebula
    """

    def ask(self, question, default):
        # since CLEO has a bug that causes it not to return default values we need a wrapper that does exactly that
        output = super(DeployCommand, self).ask(question)
        if output is None:
            output = default
        return output

    def handle(self):
        cores = self.ask('How many processing cores should the VM have? (Default 1): ', 1)
        ram = self.ask('How much memory in GiB should the VM have? (Default 4): ', 4)
        name = self.ask('What is the name of the VM? (Default generated): ', uuid.uuid4())

        deployVmCommand = DeployVm().name(name).cores(cores).ram(ram)

        cloudServices = CloudServices()
        cloudNames = cloudServices.getCloudNames()
        # for some reason cleo can not handle arrays with 1 el
        if len(cloudNames) > 1:
            cloudProviderName = self.choice('Please select a cloud provider (default: {0})'.format(cloudNames[0]), cloudNames, 0)
        else:
            cloudProviderName = cloudNames[0]

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        commandBus = cloudService.getCommandBus()
        commandBus.handle(deployVmCommand)
