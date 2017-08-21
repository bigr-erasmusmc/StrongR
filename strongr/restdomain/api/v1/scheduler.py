from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request

import strongr.core
import time
import uuid


ns = Namespace('scheduler', description='Operations related to the schedulerdomain')

task = ns.model('task', {
    'cmd': fields.String(required=True, min_length=1, description='The shellcode to be executed'),
    'cores': fields.Integer(required=True, min=1, description='The amount of cores needed to peform the task'),
    'ram': fields.Integer(required=True, min=1, description="The amount of ram in GiB needed to peform the task")
})
@ns.route('/task')
class Tasks(Resource):
    @ns.response(201, 'Task successfully created.')
    @ns.expect(task, validate=True)
    def post(self):
        """Creates a new task."""
        schedulerService = strongr.core.getCore().domains().schedulerDomain().schedulerService()
        commandFactory = strongr.core.getCore().domains().schedulerDomain().commandFactory()

        cmd = request.json['cmd']
        cores = int(request.json['cores'])
        ram = int(request.json['ram'])

        taskid = str(int(time.time())) + '-' + str(uuid.uuid4())
        command = commandFactory.newScheduleTaskCommand(taskid, cmd, cores, ram)

        schedulerService.getCommandBus().handle(command)
        return {'taskid': taskid}, 201
