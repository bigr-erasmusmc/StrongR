from strongr.clouddomain.handler.abstract.cloud import AbstractDestroyVmHandler

import salt.cloud

class DestroyVmHandler(AbstractDestroyVmHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        return client.destroy(command.name)
