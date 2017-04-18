import salt.client

class RunShellCodeHandler():
    def __call__(self, command):
        local = salt.client.LocalClient()
        result = local.cmd(vm, 'cmd.run', [cmd])
        return result
