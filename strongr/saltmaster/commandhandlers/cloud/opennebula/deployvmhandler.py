import salt.cloud

class DeployVmHandler():
    def __call__(self, command):
        configuration = command.configuration

        kwargs = {}

        if configuration.ram > 0: kwargs['memory'] = configuration.ram * 1024
        if configuration.cores > 0: kwargs['cpu'] = configuration.cores

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = ["thomas-new-testvm-" + str(i+1) for i in range(0,4)]
        vms = client.profile(names=names, profile='salt-minion', parallel=True, **kwargs)
