from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler
from strongr.clouddomain.command import DeployVm, RunShellCode, DeployVms
from strongr.clouddomain.query import ListDeployedVms

class OpenNebula(AbstractCloudService):
    def getCommandHandlers(self):
        return [DeployVmHandler, RunShellCodeHandler, DeployVmsHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler]
