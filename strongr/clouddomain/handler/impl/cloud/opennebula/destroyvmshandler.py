from strongr.clouddomain.handler.abstract.cloud import AbstractDestroyVmsHandler

import salt.cloud
import strongr.core

class DestroyVmsHandler(AbstractDestroyVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient(strongr.core.Core.config().clouddomain.OpenNebula.salt_config + '/cloud')

        ret = []
        for chunked_names in self._chunk_list(command.names, 4):
            ret.append(client.destroy(names=chunked_names))

        return ret

    def _chunk_list(self, list, chunksize):
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]

