from strongr.clouddomain.handler.abstract.cloud import AbstractListDeployedVmsHandler

import salt.cloud

class ListDeployedVmsHandler(AbstractListDeployedVmsHandler):
    def __call__(self, command):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        names = {}
        rs = client.query()

        for provider in list(rs.keys()):
            for location in list(rs[provider].keys()):
                for machine in list(rs[provider][location].keys()):
                    names[machine] = {
                        'cores': int(rs[provider][location][machine]['size']['cpu']),
                        'ram': int(rs[provider][location][machine]['size']['memory']) // 1024
                    }

        opts = salt.config.master_config('/etc/salt/master')
        opts['quiet'] = True
        runner = salt.runner.RunnerClient(opts)

        result = runner.cmd('manage.up')

        for machine in names:
            if machine not in result:
                del names[machine]

        return names
