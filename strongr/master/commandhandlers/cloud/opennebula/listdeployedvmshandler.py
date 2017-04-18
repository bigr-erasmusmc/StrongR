import salt.cloud

class ListDeployedVmsHandler():
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        rs = client.query()

        for provider in list(rs.keys()):
            print(provider)
            print(rs[provider])
            for location in list(rs[provider].keys()):
                print(location)
                names.extend(list(rs[provider][location].keys()))
        return names
