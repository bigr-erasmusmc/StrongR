from cleo import Command

from services import CloudServices
from services import CloudConfigHelpers

class ConfigHelperCommand(Command):
    """
    A configuration helper

    config:helper
    """

    def handle(self):
        cloudServices = CloudServices()

        self.info('This tool will help you generate the salt and strongr configurations')

        cloudNames = cloudServices.getCloudNames()
        if len(cloudNames) > 1:
            cloudProviderName = self.choice('Please select a cloud provider (default: {0})'.format(cloudNames[0]), cloudNames, 0)
        else:
            cloudProviderName = cloudNames[0]

        # use hardcoded strings for now
        # TODO: we should change this to something more dynamic
        if cloudProviderName == 'OpenNebula':

