import salt.cloud
import re

class DeployVmHandler():
    def __call__(self, command):
        overrides = {}

        if command.ram > 0: overrides['memory'] = command.ram * 1024

        if command.cores > 0:
            overrides['cpu'] = command.cores
            overrides['vcpu'] = command.cores

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        return client.profile(names=[command.name], profile='salt-minion', vm_overrides=overrides)
