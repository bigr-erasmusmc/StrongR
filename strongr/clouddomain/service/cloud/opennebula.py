from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.clouddomain.command import DeployVm, ListDeployedVms, RunShellCode, DeployVms

class OpenNebula(AbstractCloudService):
    def getCommandHandlers(self):
        return [DeployVmHandler, RunShellCodeHandler, DeployVmsHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler]
