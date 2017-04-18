import salt.cloud

class ListDeployedVmsHandler():
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        for provider in rs:
            for location in rs[provider].keys():
                names.append(list(rs[provider][location].keys()))
        return names
