from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = {}
        rs = client.query()

        for provider in list(rs.keys()):
            for location in list(rs[provider].keys()):
                for machine in list(rs[provider][location].keys()):
                    names[machine] = {
                        'cores': rs[provider][location][machine]['size']['cpu'],
                        'ram': rs[provider][location][machine]['size']['memory'] / 1024
                    }

        return names
