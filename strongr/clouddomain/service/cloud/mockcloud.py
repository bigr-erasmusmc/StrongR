from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.mockcloud import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.clouddomain.command import DeployVm, ListDeployedVms, RunShellCode, DeployVms

class MockCloud(AbstractCloudService):
    def setup(self):
        self.injectHandlers([DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler])
