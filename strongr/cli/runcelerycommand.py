from .wrapper import Command

import strongr.core

class RunCeleryCommand(Command):
    """
    Runs a celery worker.

    celery:run
    """
    def handle(self):
        from celery import Celery
        broker = 'amqp://guest:guest@localhost'
        celery_test = Celery('celery_test', broker=broker, backend=broker)

        scheduler = self.getDomains().schedulerDomain().schedulerService()
        scheduler.getCommandBus() # we need to initiate this so that celery knows where to send its commands
        scheduler.getQueryBus() # we need to initiate this so that celery knows where to send its commands

        commands = [
                'strongr.schedulerdomain.command.scheduletask.ScheduleTask',
                'strongr.schedulerdomain.query.requestscheduledtasks.RequestScheduledTasks'
            ]

        for command in commands:
            strongr.core.getCore().commandRouter().enable_worker_route_for_command(celery_test, command)

        argv = [
            'worker',
            '--loglevel=DEBUG',
            '-Q=' + ','.join(commands)
        ]
        celery_test.worker_main(argv)
