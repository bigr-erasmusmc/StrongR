import salt.client

class RunShellCodeHandler():
    def __call__(self, command):
        local = salt.client.LocalClient()
        result = local.cmd(command.host, 'cmd.run', [command.sh])
        return result
