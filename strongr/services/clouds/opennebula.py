from .basecloudservice import BaseCloudService

from strongr.commandhandlers.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.commands import DeployVm, ListDeployedVms, RunShellCode, DeployVms

class OpenNebula(BaseCloudService):
    def setup(self):
        self.injectHandlers({ \
            DeployVmHandler: DeployVm.__name__, \
            ListDeployedVmsHandler: ListDeployedVms.__name__, \
            RunShellCodeHandler: RunShellCode.__name__, \
            DeployVmsHandler: DeployVms.__name__
        })
