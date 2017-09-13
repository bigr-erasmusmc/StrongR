from strongr.clouddomain.handler.abstract.cloud import AbstractDeployVmsHandler

import salt.cloud

class DeployVmsHandler(AbstractDeployVmsHandler):
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

        ret = []
        for chunked_names in self._chunk_list(names, 2):
            print(chunked_names)
            #ret.append(client.profile(names=chunked_names, profile='salt-minion', vm_overrides=overrides, parallel=True))

        return ret


    def _chunk_list(self, list, chunksize):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]
