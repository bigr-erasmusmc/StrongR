from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.opennebula import DeployVmHandler, ListDeployedVmsHandler,\
                                                                RunShellCodeHandler, DeployVmsHandler,\
                                                                RequestJidStatusHandler, DestroyVmHandler

class OpenNebula(AbstractCloudService):
    def getCommandHandlers(self):
        return [DeployVmHandler, RunShellCodeHandler, DeployVmsHandler, DestroyVmHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler, RequestJidStatusHandler]
