from strongr.clouddomain.handler.abstract.cloud import AbstractRequestJidStatusHandler

import salt.runner

class RequestJidStatusHandler(AbstractRequestJidStatusHandler):
    def __call__(self, query):
        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        result = runner.cmd('jobs.lookup_jid', [query.jid])
        return result
