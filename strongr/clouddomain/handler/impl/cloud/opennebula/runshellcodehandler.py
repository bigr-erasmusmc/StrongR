from strongr.clouddomain.handler.abstract.cloud import AbstractRunShellCodeHandler
import strongr.core

import salt.client

class RunShellCodeHandler(AbstractRunShellCodeHandler):
    def __call__(self, command):
        local = salt.client.LocalClient()
        local.cmd_async(command.host, 'cmd.run', [command.sh, "runas={}".format(strongr.core.Core.config().clouddomain.OpenNebula.runas)], jid=command.job_id)
