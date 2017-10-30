import threading

import fnmatch
import salt.config
import salt.utils.event

import strongr.core
from strongr.clouddomain.handler.impl.cloud.opennebula import ListDeployedVmsHandler, \
    RunShellCodeHandler, DeployVmsHandler, \
    RequestJidStatusHandler, DestroyVmsHandler
from .abstractcloudservice import AbstractCloudService


class SaltEventTranslator(threading.Thread):
    def run(self):
        opts = salt.config.client_config(strongr.core.Core.config().clouddomain.OpenNebula.salt_config + '/master')

        event = salt.utils.event.get_event(
            'master',
            sock_dir=opts['sock_dir'],
            transport=opts['transport'],
            opts=opts)

        while True:
            ret = event.get_event(full=True)
            if ret is None:
                continue

            if fnmatch.fnmatch(ret['tag'], 'salt/job/*/ret/*'):
                data = ret['data']
                if 'jid' in data and 'return' in data and 'retcode' in data:
                    pass
                    #job_finished_event = JobFinished(data['jid'], data['return'], data['retcode'])
                    #strongr.core.Core.domainEventsPublisher().publish(job_finished_event)

class OpenNebula(AbstractCloudService):
    _salt_event_translator_thread = None

    def __init__(self, *args, **kwargs):
        super(OpenNebula, self).__init__(*args, **kwargs)
        if self._salt_event_translator_thread is None or not self._salt_event_translator_thread.is_alive():
            self._salt_event_translator_thread = SaltEventTranslator(name="SaltEventTranslator")
            self._salt_event_translator_thread.start()

    def getCommandHandlers(self):
        return [RunShellCodeHandler, DeployVmsHandler, DestroyVmsHandler]

    def getQueryHandlers(self):
        return [ListDeployedVmsHandler, RequestJidStatusHandler]
