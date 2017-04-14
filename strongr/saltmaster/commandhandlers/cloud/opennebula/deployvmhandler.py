import salt.cloud
import re

class DeployVmHandler():
    def __call__(self, command):
        kwargs = {}

        if command.ram > 0: kwargs['memory'] = command.ram * 1024
        if command.cores > 0: kwargs['cpu'] = command.cores

        command.name = re.sub(r'[^a-zA-Z0-9]*', '', command.name)
        print(command.name)
        return

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        vm = client.profile(names=[command.name], profile='salt-minion', **kwargs)
        print(vm)
