from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        for provider in list(rs.keys()):
            for location in list(rs[provider].keys()):
                for machine in list(rs[provider][location].keys()):
                    print(rs[provider][location][machine])
        #return names
