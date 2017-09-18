from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.opennebula import ListDeployedVmsHandler,\
                                                                RunShellCodeHandler, DeployVmsHandler,\
                                                                RequestJidStatusHandler, DestroyVmsHandler

class OpenNebula(AbstractCloudService):
    def getCommandHandlers(self):
        return [RunShellCodeHandler, DeployVmsHandler, DestroyVmsHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler, RequestJidStatusHandler]
