from strongr.domain.commandhandlers.abstract.cloud import AbstractRunShellCodeHandler

import salt.client

class RunShellCodeHandler(AbstractRunShellCodeHandler):
    def __call__(self, command):
        local = salt.client.LocalClient()
        result = local.cmd(command.host, 'cmd.run', [command.sh])
        return result
