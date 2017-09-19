from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmsHandler

import salt.cloud
import time

import strongr.core

class DeployVmsHandler(AbstractDeployVmsHandler):
    def __call__(self, command):
        overrides = {}

        if command.ram > 0:
            overrides['memory'] = command.ram * 1024

        if command.cores > 0:
            overrides['cpu'] = command.cores
            overrides['vcpu'] = command.cores

        client = salt.cloud.CloudClient(strongr.core.Core.config().clouddomain.OpenNebula.salt_config + '/cloud')

        ret = []
        for chunked_names in self._chunk_list(command.names, 2):
            ret.append(client.profile(names=chunked_names, profile=strongr.core.Core.config().clouddomain.OpenNebula.profile, vm_overrides=overrides, parallel=True))
            time.sleep(60)

        return ret


    def _chunk_list(self, list, chunksize):
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]
