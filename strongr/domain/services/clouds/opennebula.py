from .abstractcloudservice import AbstractCloudService

from strongr.domain.commandhandlers.impl.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.domain.commands import DeployVm, ListDeployedVms, RunShellCode, DeployVms

class OpenNebula(AbstractCloudService):
    def setup(self):
        self.injectHandlers([DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler])
