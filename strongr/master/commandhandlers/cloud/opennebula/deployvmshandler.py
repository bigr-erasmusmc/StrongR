import salt.cloud

class DeployVmsHandler:
    def __call__(self, commands):
        names = []
        for deployCommand in commands:
            names.append(deployCommand.name)

        overrides = {}

        if commands[0].ram > 0:
            overrides['memory'] = commands[0].ram * 1024

        if commands[0].cores > 0:
            overrides['cpu'] = commands[0].cores
            overrides['vcpu'] = commands[0].cores

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        return client.profile(names=[names], profile='salt-minion', vm_overrides=overrides, parallel=True)
