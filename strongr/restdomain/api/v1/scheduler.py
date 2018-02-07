from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request

import strongr.core
import time
import uuid

import strongr.restdomain.model.gateways
from strongr.core.domain.schedulerdomain import SchedulerDomain
from strongr.restdomain.api.utils import namespace_require_oauth

ns = Namespace('scheduler', description='Operations related to the schedulerdomain')

post_task = ns.model('post-task', {
    'cmd': fields.String(required=True, min_length=1, description='The shellcode to be executed'),
    'cores': fields.Integer(required=True, min=1, description='The amount of cores needed to peform the task'),
    'ram': fields.Integer(required=True, min=1, description="The amount of ram in GiB needed to peform the task")
})

@ns.route('/task')
class Tasks(Resource):
    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)

    @ns.response(200, 'OK')
    @namespace_require_oauth('task')
    @ns.param('task_id')
    def get(self):
        """Requests task status"""
        schedulerService = SchedulerDomain.schedulerService()
        queryFactory = SchedulerDomain.queryFactory()

        query = queryFactory.newRequestScheduledJobs()

        result = schedulerService.getQueryBus().handle(query)
        return result, 200

    @ns.response(201, 'Task successfully created.')
    @namespace_require_oauth('task')
    @ns.expect(post_task, validate=True)
    def post(self):
        """Creates a new task."""
        schedulerService = SchedulerDomain.schedulerService()
        commandFactory = SchedulerDomain.commandFactory()

        cmd = request.json['cmd']
        cores = int(request.json['cores'])
        ram = int(request.json['ram'])
        taskid = str(int(time.time())) + '-' + str(uuid.uuid4())

        command = commandFactory.newScheduleJobCommand(taskid, cmd, cores, ram)

        schedulerService.getCommandBus().handle(command)
        return {'taskid': taskid}, 201
