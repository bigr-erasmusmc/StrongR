import salt.cloud

class ListDeployedVmsHandler():
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = []
        for cloudEnv in client.query().keys():
            names.append(list(cloudEnv.keys()))
        return names
