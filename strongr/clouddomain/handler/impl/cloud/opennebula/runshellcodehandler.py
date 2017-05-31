from strongr.clouddomain.handler.abstract.cloud import AbstractRunShellCodeHandler

import salt.client

class RunShellCodeHandler(AbstractRunShellCodeHandler):
    def __call__(self, command):
        local = salt.client.LocalClient()
        #result = local.cmd_async(command.host, 'cmd.run', [command.sh], runas="ubuntu")
        result = local.cmd_async(command.host, 'cmd.run', ['whoami'], runas="ubuntu")
        return result
