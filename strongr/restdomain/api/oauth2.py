import strongr.core
import strongr.core.domain.restdomain
from flask_oauthlib.provider import OAuth2Provider

from datetime import datetime, timedelta

from flask import make_response, jsonify, g

from strongr.restdomain.model.oauth2 import Token
from strongr.core.gateways import Gateways

core = strongr.core.Core
rest_domain = strongr.core.domain.restdomain.RestDomain

oauth2_service = rest_domain.oauth2Service()
oauth2_command_factory = rest_domain.oauth2CommandFactory()
oauth2_command_bus = oauth2_service.getCommandBus()

oauth2_query_factory = rest_domain.oauth2QueryFactory()
oauth2_query_bus = oauth2_service.getQueryBus()

def bind_oauth2(app):
    oauth = OAuth2Provider(app)

    @oauth.clientgetter
    def get_client(client_id):
        print('get_client')
        return oauth2_query_bus.handle(oauth2_query_factory.newRetrieveClient(client_id))

    @oauth.grantgetter
    def get_grant(client_id, code):
        print('get_grant')
        return oauth2_query_bus.handle(oauth2_query_factory.newRetrieveGrant(client_id, code))

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        print('get_token')
        if access_token:
            return oauth2_query_bus.handle(oauth2_query_factory.newRetrieveTokenByAccessToken(access_token))
        if refresh_token:
            return oauth2_query_bus.handle(oauth2_query_factory.newRetrieveTokenByRefreshToken(refresh_token))
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        print('set_grant')
        expires = datetime.utcnow() + timedelta(seconds=600)
        oauth2_command_bus.handle(oauth2_command_factory.newAppendGrant(
                client_id=client_id,
                code=code['code'],
                redirect_uri=request.redirect_uri,
                scope=' '.join(request.scopes),
                user_id=g.user.id,
                expires=expires
            ))

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        print('set_token')
        # In real project, a token is unique bound to user and client.
        # Which means, you don't need to create a token every time.
        tok = Token(**token)
        tok.user_id = request.user.id
        tok.client_id = request.client.client_id
        session = Gateways.sqlalchemy_session()
        session.add(tok)
        session.commit()

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
    #    # This is optional, if you don't need password credential
    #    # there is no need to implement this method
        print('get_user')
    #    return User.query.filter_by(username=username).first()

    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(request, *args, **kwargs):
        print('authorize_request')
        # NOTICE: for real project, you need to require login
        #if request.method == 'GET':
            # render a page for user to confirm the authorization
        #    return render_template('confirm.html')

        if request.method == 'HEAD':
            # if HEAD is supported properly, request parameters like
            # client_id should be validated the same way as for 'GET'
            response = make_response('', 200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response

        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'

    @app.route('/oauth/token', methods=['POST', 'GET'])
    @oauth.token_handler
    def access_token():
        print('access_token')
        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        print('revoke_token')
        pass

    @oauth.invalid_response
    def require_oauth_invalid(req):
        print('require_oauth_invalid')
        return jsonify(message=req.error_message), 401

    return oauth
