from strongr.clouddomain.handler.abstract.cloud import AbstractRunJobHandler
import sys

from strongr.clouddomain.model.gateways import Gateways

if sys.version_info[0] > 3 and sys.version_info[1] > 3:
    # python > 3.3 uses shlex.quote
    from shlex import quote
else:
    from pipes import quote

import os
import subprocess
import tempfile

import threading
import strongr.core

class RunJobHandler(AbstractRunJobHandler):
    def __call__(self, command):
        thread = threading.Thread(target=self._run, args=(command,)) # run in separate thread so it doesn't block strongr
        thread.start()
        #self._run(command)

    def _run(self, command):
        inter_domain_event_factory = Gateways.inter_domain_event_factory()
        inter_domain_events_publisher = strongr.core.Core.inter_domain_events_publisher()

        volumes = ''
        env = ''
        if command.scratch:
            if not os.path.isdir('/tmp/strongr_scratch'):
                os.mkdir('/tmp/strongr_scratch', 0700)

            volumes = '--volume=/tmp/strongr_scratch:/scratch'
            env = "-e SCRATCH_DIR='/scratch'"


        cmd = 'docker run --rm {} {} -di --name {} -m {}g --cpus={} --entrypoint /bin/sh {}'.format(volumes, env, command.job_id, command.memory, command.cores, quote(command.image))
        ret_code = subprocess.call(cmd, shell=True) # start docker container

        if ret_code != 0:
            raise Exception('Something went wrong while initializing docker image: {}'.format(cmd))

        tmpfile = tempfile.mkstemp()[1]
        fh = open(tmpfile, 'w')
        fh.write("\n".join(command.script))
        fh.close()

        cmd = 'docker exec -i {} /bin/sh < {}'.format(command.job_id, tmpfile)
        try:
            stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            job_finished_event = inter_domain_event_factory.newJobFinishedEvent(command.job_id, err.output, err.returncode)
            inter_domain_events_publisher.publish(job_finished_event)
            if ret_code != 0:
                Exception('Something went wrong while executing script in docker image: {}'.format(cmd))
            stdout = err.output

        os.remove(tmpfile)


        cmd = 'docker stop {}'.format(command.job_id)
        ret_code = subprocess.call(cmd, shell=True)

        if ret_code != 0:
            raise Exception('Something went wrong while stopping docker image: {}'.format(cmd))



        job_finished_event = inter_domain_event_factory.newJobFinishedEvent(command.job_id, stdout, 0)
        inter_domain_events_publisher.publish(job_finished_event)