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
        intra_domain_event_factory = strongr.clouddomain.model.gateways.Gateways.intra_domain_event_factory()
        inter_domain_event_factory = strongr.clouddomain.model.gateways.Gateways.intra_domain_event_factory()

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
                    salt_job_finished_event = intra_domain_event_factory.newSaltJobFinished(data['jid'], data['return'], data['retcode'])
                    strongr.clouddomain.model.gateways.Gateways.intra_domain_events_publisher().publish(salt_job_finished_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/creating'):
                if 'name' in data:
                    vmcreated_event = inter_domain_event_factory.newVmCreatedEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmcreated_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/created'):
                if 'name' in data:
                    vmready_event = inter_domain_event_factory.newVmReadyEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmready_event)
            elif fnmatch.fnmatch(ret['tag'], 'salt/cloud/*/destroyed'):
                if 'name' in data:
                    vmready_event = inter_domain_event_factory.newVmReadyEvent(data['name'])
                    strongr.core.Core.inter_domain_events_publisher().publish(vmready_event)
