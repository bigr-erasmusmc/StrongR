from .basecloudservice import BaseCloudService

from commandhandlers.cloud.opennebula import DeployVmHandler
from commandhandlers.cloud.opennebula import ListDeployedVmsHandler
from commandhandlers.cloud.opennebula import RunShellCodeHandler
from commandhandlers.cloud.opennebula import DeployVmsHandler

from commands import DeployVm
from commands import ListDeployedVms
from commands import RunShellCode
from commands import DeployVms

class OpenNebula(BaseCloudService):
    def setup(self):
        self.injectHandlers({ \
            DeployVmHandler: DeployVm.__name__, \
            ListDeployedVmsHandler: ListDeployedVms.__name__, \
            RunShellCodeHandler: RunShellCode.__name__, \
            DeployVmsHandler: DeployVms.__name__
        })
