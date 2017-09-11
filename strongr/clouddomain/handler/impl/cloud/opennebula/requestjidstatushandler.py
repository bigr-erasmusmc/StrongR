from strongr.clouddomain.handler.abstract.cloud import AbstractRequestJidStatusHandler

import strongr.core
import salt.runner

class RequestJidStatusHandler(AbstractRequestJidStatusHandler):
    def __call__(self, query):
        opts = salt.config.master_config('/etc/salt/master')
        opts['quiet'] = True
        runner = salt.runner.RunnerClient(opts)

        core = strongr.core.getCore()
        cache = core.cache()

        if not cache.exists('clouddomain.jobs.running'):
            cache.set('clouddomain.jobs.running', runner.cmd('jobs.active'), 1)

        jobs = cache.get('clouddomain.jobs.running')

        if query.jid not in jobs: # we only want to give status when the job is finished running
            result = runner.cmd('jobs.lookup_jid', [query.jid])
            return result
        return None
