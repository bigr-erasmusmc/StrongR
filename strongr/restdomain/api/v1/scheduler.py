from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request

from strongr.restdomain.api.utils import blueprint_require_oauth

import strongr.core
import time
import uuid

ns = Namespace('scheduler', description='Operations related to the schedulerdomain')

post_task = ns.model('post-task', {
    'cmd': fields.String(required=True, min_length=1, description='The shellcode to be executed'),
    'cores': fields.Integer(required=True, min=1, description='The amount of cores needed to peform the task'),
    'ram': fields.Integer(required=True, min=1, description="The amount of ram in GiB needed to peform the task")
})
@ns.route('/task')
class Tasks(Resource):
    @ns.response(200, 'OK')
    def get(self):
        schedulerService = strongr.core.getCore().domains().schedulerDomain().schedulerService()
        queryFactory = strongr.core.getCore().domains().schedulerDomain().queryFactory()

        from celery import Celery
        broker = 'amqp://guest:guest@localhost'
        celery_test = Celery('celery_test', broker=broker, backend=broker)

        query = queryFactory.newRequestScheduledTasks()

        strongr.core.getCore().commandRouter().enable_route_for_command(celery_test, query.__module__ + '.' + query.__class__.__name__)
        result = schedulerService.getQueryBus().handle(query)
        return result, 200

    @ns.response(201, 'Task successfully created.')
    #@blueprint_require_oauth('task')
    @ns.expect(post_task, validate=True)
    def post(self):
        """Creates a new task."""
        schedulerService = strongr.core.getCore().domains().schedulerDomain().schedulerService()
        commandFactory = strongr.core.getCore().domains().schedulerDomain().commandFactory()

        cmd = request.json['cmd']
        cores = int(request.json['cores'])
        ram = int(request.json['ram'])

        taskid = str(int(time.time())) + '-' + str(uuid.uuid4())
        command = commandFactory.newScheduleTaskCommand(taskid, cmd, cores, ram)

        from celery import Celery
        broker = 'amqp://guest:guest@localhost'
        celery_test = Celery('celery_test', broker=broker, backend=broker)
        strongr.core.getCore().commandRouter().enable_route_for_command(celery_test, command.__module__ + '.' + command.__class__.__name__)

        schedulerService.getCommandBus().handle(command)
        return {'taskid': taskid}, 201
