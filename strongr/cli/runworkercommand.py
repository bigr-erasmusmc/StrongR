from celery.signals import worker_process_init

from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import strongr.core
from celery import Celery

class RunWorkerCommand(Command):
    """
    Runs a strongr worker.

    worker:run
        {--p|profile=elasticworker : The worker profile to be used}
    """
    def handle(self):
        config = strongr.core.Core.config()
        broker = config.celery.broker
        backend = config.celery.backend

        celery = Celery('strongr', broker=broker, backend=backend)

        scheduler = SchedulerDomain.schedulerService()
        scheduler.getCommandBus() # we need to initiate this so that celery knows where to send its commands
        scheduler.getQueryBus() # we need to initiate this so that celery knows where to send its commands

        domains = getattr(config.celery.workers, self.option('profile')).as_dict()

        commands = []
        for domain in domains:
            for command in domains[domain]:
                commands.append('{}.{}'.format(domain, command))

        for command in commands:
            strongr.core.Core.command_router().enable_worker_route_for_command(celery, command)

        argv = [
            'worker',
            '--loglevel=DEBUG',
            '-Q=' + ','.join(commands)
        ]

        @worker_process_init.connect
        def fix_multiprocessing(**kwargs):
            # don't be a daemon, so we can create new subprocesses
            from multiprocessing import current_process
            current_process().daemon = False
            
        celery.worker_main(argv)
