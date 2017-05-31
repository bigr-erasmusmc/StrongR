from strongr.clouddomain.handler.abstract.cloud import AbstractRequestJidStatusHandler

import salt.cloud

class RequestJidStatusHandler(AbstractRequestJidStatusHandler):
    def __call__(self, query):
        runner = salt.client.RunnerClient()
        result = runner.cmd('jobs.lookup_jid', query.jid)
        return result