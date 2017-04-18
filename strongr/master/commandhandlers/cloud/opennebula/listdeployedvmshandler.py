import salt.cloud

class ListDeployedVmsHandler():
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        for provider in list(rs.keys()):
            for location in list(rs[provider].keys()):
                names.extend(list(rs[provider][location].keys()))
        return names
