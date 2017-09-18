from .abstractcloudservice import AbstractCloudService

from strongr.clouddomain.handler.impl.cloud.mockcloud import ListDeployedVmsHandler, RunShellCodeHandler, DeployVmsHandler

class MockCloud(AbstractCloudService):

    def getCommandHandlers(self):
        return [RunShellCodeHandler, DeployVmsHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler]
