import salt.cloud
import re

class DeployVmHandler():
    def __call__(self, command):
        kwargs = {}

        if command.ram > 0: kwargs['memory'] = command.ram * 1024
        if command.cores > 0: kwargs['cpu'] = command.cores

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        return client.create(names=[command.name], profile='salt-minion', **kwargs)
