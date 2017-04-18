import salt.cloud

class DeployVmsHandler:
    def __call__(self, commands):
        names = []
        for deployCommand in commands:
            names.append(deployCommand.name)

        overrides = {}

        if command[0].ram > 0:
            overrides['memory'] = command[0].ram * 1024

        if command[0].cores > 0:
            overrides['cpu'] = command[0].cores
            overrides['vcpu'] = command[0].cores

        print(overrides)
        print(names)
        return

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        return client.profile(names=[names], profile='salt-minion', vm_overrides=overrides, parallel=True)
