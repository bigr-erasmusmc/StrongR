from salt.exceptions import SaltSystemExit

from strongr.clouddomain.handler.abstract.cloud import AbstractDestroyVmsHandler

import salt.cloud
import strongr.core

import logging

class DestroyVmsHandler(AbstractDestroyVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient(strongr.core.Core.config().clouddomain.OpenNebula.salt_config + '/cloud')

        logger = logging.getLogger(self.__class__.__name__)

        ret = []
        for chunked_names in self._chunk_list(command.names, 1):
            try:
                ret.append(client.destroy(names=chunked_names))
            except SaltSystemExit as e:
                # an exception occured within salt, normally below event would be published trough salt event system
                # assume VM is no longer there and broadcast vm destroyed event from here
                # if it turns out the vm still there but error was triggered due to api rate limiting or flaky connection
                # the cleanup script will remove the vm at a later time but this cleanup script will not trigger below event
                inter_domain_event_factory = strongr.clouddomain.model.gateways.Gateways.inter_domain_event_factory()
                vmdestroyed_event = inter_domain_event_factory.newVmDestroyedEvent(chunked_names[0])
                strongr.core.Core.inter_domain_events_publisher().publish(vmdestroyed_event)
                logger.warning(e)

        return ret

    def _chunk_list(self, list, chunksize):
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]
