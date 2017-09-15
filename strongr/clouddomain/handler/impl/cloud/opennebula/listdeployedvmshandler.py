from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud
import strongr.core

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        core = strongr.core.getCore()

        client = salt.cloud.CloudClient(core.config().clouddomain.OpenNebula.salt_config + '/cloud')
        names = {}
        rs = client.query()

        for provider in list(rs.keys()):
            for location in list(rs[provider].keys()):
                for machine in list(rs[provider][location].keys()):
                    names[machine] = {
                        'cores': int(rs[provider][location][machine]['size']['cpu']),
                        'ram': int(rs[provider][location][machine]['size']['memory']) // 1024
                    }

        opts = salt.config.master_config(core.config().clouddomain.OpenNebula.salt_config + '/master')
        opts['quiet'] = True
        runner = salt.runner.RunnerClient(opts)

        result = runner.cmd('manage.up')

        for machine in list(names):
            if machine not in result:
                del names[machine]

        return names
