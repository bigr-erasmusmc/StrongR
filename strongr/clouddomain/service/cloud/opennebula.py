from .abstractcloudservice import AbstractCloudService

from strongr.cloudDomain.handler.impl.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.cloudDomain.command import DeployVm, ListDeployedVms, RunShellCode, DeployVms

class OpenNebula(AbstractCloudService):
    def setup(self):
        self.injectHandlers([DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler])
