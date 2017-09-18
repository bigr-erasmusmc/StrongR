from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmHandler

#from strongr.clouddomain.event import NewVmDeployed

import strongr.core

import salt.cloud

class DeployVmHandler(AbstractDeployVmHandler):
    def __call__(self, command):
        core = strongr.core.getCore()
        overrides = {}

        if command.ram > 0: overrides['memory'] = command.ram * 1024

        if command.cores > 0:
            overrides['cpu'] = command.cores
            overrides['vcpu'] = command.cores

        client = salt.cloud.CloudClient(core.config().clouddomain.OpenNebula.salt_config + '/cloud')
        client.profile(names=[command.name], profile=core.config().clouddomain.OpenNebula.profile, vm_overrides=overrides)
        #self.publishDomainEvent(command.name, command.cores, command.ram)
