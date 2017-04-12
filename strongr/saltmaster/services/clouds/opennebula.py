from .basecloudservice import BaseCloudService

from commandhandlers.cloud.opennebula import DeployVmHandler

from commands import DeployVm

class OpenNebula(BaseCloudService):
    def setup(self):
        self.injectHandlers({ \
            DeployVmHandler: DeployVm.__name__, \
        })
