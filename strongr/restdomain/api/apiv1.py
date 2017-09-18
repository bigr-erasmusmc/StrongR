from flask import Blueprint
from flask_restplus import Api

from strongr.restdomain.api.v1.scheduler import ns as scheduler_namespace

blueprint = Blueprint('api_v1', __name__, url_prefix='/v1')
api = Api(blueprint,
    title='V1 Api',
    version='1.0',
    description='First version of the API'
)

api.add_namespace(scheduler_namespace)
