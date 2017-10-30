from strongr.core.domain.schedulerdomain import SchedulerDomain
from .wrapper import Command

import strongr.core
from celery import Celery

class RunCeleryCommand(Command):
    """
    Runs a celery worker.

    celery:run
    """
    def handle(self):
        config = strongr.core.Core.config()
        broker = config.celery.broker
        backend = config.celery.backend

        celery = Celery('celery_test', broker=broker, backend=backend)

        scheduler = SchedulerDomain.schedulerService()
        scheduler.getCommandBus() # we need to initiate this so that celery knows where to send its commands
        scheduler.getQueryBus() # we need to initiate this so that celery knows where to send its commands

        commands = config.celery.enabled_routes

        for command in commands:
            strongr.core.Core.command_router().enable_worker_route_for_command(celery, command)

        argv = [
            'worker',
            '--loglevel=DEBUG',
            '-Q=' + ','.join(commands)
        ]
        celery.worker_main(argv)
