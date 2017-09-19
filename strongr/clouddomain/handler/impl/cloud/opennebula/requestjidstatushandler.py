from strongr.clouddomain.handler.abstract.cloud import AbstractRequestJidStatusHandler

import strongr.core
import salt.runner

import strongr.core
from strongr.core.gateways import Gateways

class RequestJidStatusHandler(AbstractRequestJidStatusHandler):
    def __call__(self, query):
        core = strongr.core.getCore()
        opts = salt.config.master_config(core.config().clouddomain.OpenNebula.salt_config + '/master')
        opts['quiet'] = True
        runner = salt.runner.RunnerClient(opts)

        cache = Gateways.cache()

        if not cache.exists('clouddomain.jobs.running'):
            cache.set('clouddomain.jobs.running', runner.cmd('jobs.active'), 1)

        jobs = cache.get('clouddomain.jobs.running')

        if jobs is None:
            jobs = {}

        if query.jid not in jobs: # we only want to give status when the job is finished running
            result = runner.cmd('jobs.lookup_jid', [query.jid])
            return result
        return None
