import threading

import fnmatch
import salt.config
import salt.utils.event

import strongr.core

import strongr.clouddomain.factory.intradomaineventfactory
import strongr.clouddomain.factory.interdomaineventfactory
import strongr.clouddomain.model.gateways

class SaltEventTranslator(threading.Thread):
    def run(self):
        opts = salt.config.client_config(strongr.core.Core.config().clouddomain.OpenNebula.salt_config + '/master')
        inter_domain_event_factory = strongr.clouddomain.model.gateways.Gateways.inter_domain_event_factory()

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
                if 'jid' in data and 'return' in data and 'retcode' in data and data['jid'] and data['return'] and data['retcode']:
                    job_finished_event = inter_domain_event_factory.newJobFinishedEvent(data['jid'], data['return'], data['retcode'])
                    strongr.core.Core.inter_domain_events_publisher().publish(job_finished_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/creating'):
                data = ret['data']
                if 'name' in data and data['name']:
                    vmcreated_event = inter_domain_event_factory.newVmCreatedEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmcreated_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/created'):
                data = ret['data']
                if 'name' in data and data['name']:
                    vmready_event = inter_domain_event_factory.newVmReadyEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmready_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/destroyed'):
                data = ret['data']
                if 'name' in data and data['name']:
                    vmdestroyed_event = inter_domain_event_factory.newVmReadyEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmdestroyed_event)
