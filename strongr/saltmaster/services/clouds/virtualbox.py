from .basecloudservice import BaseCloudService

from commandhandlers.cloud.virtualbox import DeployVmHandler

from commands import DeployVm

class VirtualBox(BaseCloudService):
    def setup(self):
        self.injectHandlers({ \
            DeployVmHandler: DeployVm.__name__, \
        })
