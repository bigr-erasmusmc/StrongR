from strongr.clouddomain.handler.abstract.cloud import AbstractDestroyVmHandler

import salt.cloud
import strongr.core

class DestroyVmHandler(AbstractDestroyVmHandler):
    def __call__(self, command):
        core = strongr.core.getCore()
        client = salt.cloud.CloudClient(core.config().clouddomain.OpenNebula.salt_config + '/cloud')
        client.destroy(command.name)
