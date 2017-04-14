from cleo import Command

from services import CloudServices
from services import CloudConfigHelpers

from .opennebulaconfighelper import OpenNebulaConfigHelper

class ConfigHelperCommand(Command):
    """
    A global configuration helper

    config:helper
    """

    def handle(self):
        cloudServices = CloudServices()

        self.info('This tool will help you generate the salt and strongr configurations')


        # use hardcoded strings for now
        # TODO: we should change this to something more dynamic
        if cloudProviderName == 'OpenNebula':
            self.call('config:opennebulahelper', [])
