from .basecloudservice import BaseCloudService

from commandhandlers.cloud.opennebula import DeployVmHandler
from commandhandlers.cloud.opennebula import ListDeployedVmsHandler

from commands import DeployVm
from commands import ListDeployedVms

class OpenNebula(BaseCloudService):
    def setup(self):
        self.injectHandlers({ \
            DeployVmHandler: DeployVm.__name__, \
            ListDeployedVmsHandler: ListDeployedVms.__name__
        })
