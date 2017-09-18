from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmsHandler

import salt.cloud
import time
import strongr.core

class DeployVmsHandler(AbstractDeployVmsHandler):
    def __call__(self, commands):
        core = strongr.core.getCore()
        names = []
        for deployCommand in commands:
            names.append(deployCommand.name)

        overrides = {}

        if commands[0].ram > 0:
            overrides['memory'] = commands[0].ram * 1024

        if commands[0].cores > 0:
            overrides['cpu'] = commands[0].cores
            overrides['vcpu'] = commands[0].cores

        client = salt.cloud.CloudClient(core.config().clouddomain.OpenNebula.salt_config + '/cloud')

        ret = []
        for chunked_names in self._chunk_list(names, 2):
            ret.append(client.profile(names=chunked_names, profile=core.config().clouddomain.OpenNebula.profile, vm_overrides=overrides, parallel=True))
            time.sleep(60)

        return ret


    def _chunk_list(self, list, chunksize):
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]
