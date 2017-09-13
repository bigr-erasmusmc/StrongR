from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        return rs
