from strongr.clouddomain.handler.abstract.cloud import AbstractRunJobHandler
import strongr.core

import salt.client
import base64

import sys
if sys.version_info[0] > 3 and sys.version_info[1] > 3:
    # python > 3.3 uses shlex.quote
    from shlex import quote
else:
    from pipes import quote


class DockerRunJobHandler(AbstractRunJobHandler):
    def __call__(self, command):
        volumes = ''
        env = ''
        if command.scratch:
            volumes = '--volume={}:/scratch'.format(strongr.core.Core.config().clouddomain.OpenNebula.scratchdir)
            env = "-e SCRATCH_DIR='/scratch'"

        script = "docker run --rm {} {} -di --name {} -m {}g --cpus={} --entrypoint /bin/sh {}\n".format(volumes, env,
                                                                                                    command.job_id,
                                                                                                    command.memory,
                                                                                                    command.cores,
                                                                                                    quote(command.image))
        script += "echo '{}' | base64 -d /tmp/{}\n".format(base64.b64encode(command.script), command.job_id)
        script += "docker exec -i {} /bin/sh < {}\n".format(command.job_id, '/tmp/{}'.format(command.job_id))
        script += "rm /tmp/{}\n".format(command.job_id)
        script += "docker stop {}\n".format(command.job_id)

        local = salt.client.LocalClient()
        local.cmd_async(command.host, 'cmd.run', [script, "runas={}".format(strongr.core.Core.config().clouddomain.OpenNebula.runas)], jid=command.job_id)
