from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmHandler

from strongr.clouddomain.event import NewVmDeployed

import salt.cloud

class DeployVmHandler(AbstractDeployVmHandler):
    def __call__(self, command):
        overrides = {}

        if command.ram > 0: overrides['memory'] = command.ram * 1024

        if command.cores > 0:
            overrides['cpu'] = command.cores
            overrides['vcpu'] = command.cores

        client = salt.cloud.CloudClient('/etc/salt/cloud')
        client.profile(names=[command.name], profile='salt-minion', vm_overrides=overrides)
        #self.publishDomainEvent(command.name, command.cores, command.ram)
