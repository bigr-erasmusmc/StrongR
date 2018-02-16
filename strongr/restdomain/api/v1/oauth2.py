from flask import url_for, request
from flask_restplus import Namespace, Resource

import strongr.restdomain.model.gateways
from strongr.restdomain.model.oauth2 import Client

ns = Namespace('oauth', description='Operations related to oauth2 login')

@ns.route('/revoke', methods=['POST'])
class Revoke(Resource):
    def post(self):
        auth_server = strongr.restdomain.model.gateways.Gateways.auth_server()
        return auth_server.create_revocation_response()

@ns.route('/token', methods=['POST'])
class Token(Resource):
    def post(self):
        auth_server = strongr.restdomain.model.gateways.Gateways.auth_server()
        return auth_server.create_token_response()
