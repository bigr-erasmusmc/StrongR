from strongr.clouddomain.handler.abstract.cloud import AbstractRequestJidStatusHandler

import salt.runner

class RequestJidStatusHandler(AbstractRequestJidStatusHandler):
    def __call__(self, query):
        opts = salt.config.master_config('/etc/salt/master')
        opts['quiet'] = True
        runner = salt.runner.RunnerClient(opts)

        jobs = runner.cmd('jobs.active')

        if query.jid not in jobs: # we only want to give status when the job is finished running
            result = runner.cmd('jobs.lookup_jid', [query.jid])
            return result
        return None
