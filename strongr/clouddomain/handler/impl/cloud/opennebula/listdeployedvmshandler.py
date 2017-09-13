from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        #for provider in list(rs.keys()):
        #    for location in list(rs[provider].keys()):
        #        names.extend(list(rs[provider][location].keys()))
        #return names
        return rs
