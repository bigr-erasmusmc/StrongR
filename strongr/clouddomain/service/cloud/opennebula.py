from strongr.clouddomain.handler.impl.cloud.opennebula import ListDeployedVmsHandler, \
    DeployVmsHandler, \
    RequestJidStatusHandler, DestroyVmsHandler, \
    JobFinishedHandler

from strongr.clouddomain.handler.impl.cloud.opennebula.dockerrunjobhandler import DockerRunJobHandler
from strongr.clouddomain.handler.impl.cloud.opennebula.modulesrunjobhandler import ModulesRunJobHandler

from .abstractcloudservice import AbstractCloudService

import strongr.clouddomain.model.gateways
import strongr.core

class OpenNebula(AbstractCloudService):
    _salt_event_translator_thread = None

    def __init__(self, *args, **kwargs):
        super(OpenNebula, self).__init__(*args, **kwargs)

    def start_reactor(self):
        salt_event_translator = strongr.clouddomain.model.gateways.Gateways.salt_event_translator()
        if not salt_event_translator.is_alive():
            salt_event_translator.setDaemon(True)
            salt_event_translator.start()  # start event translator thread if it wasn't running

    def get_command_handlers(self):
        # select containerization driver
        if strongr.core.Core.config().clouddomain.OpenNebula.containerization == 'modules':
            RunJobHandler = ModulesRunJobHandler
        else:
            RunJobHandler = DockerRunJobHandler

        return [RunJobHandler, DeployVmsHandler, DestroyVmsHandler, JobFinishedHandler]

    def get_query_handlers(self):
        return [ListDeployedVmsHandler, RequestJidStatusHandler]
