from flask_oauthlib.provider import OAuth2Provider
from flask import request, jsonify, make_response
from datetime import datetime, timedelta
from flask import g

from strongr.restdomain.model.oauth2 import User


def bind_oauth2(app):
    oauth = OAuth2Provider(app)

    from strongr.core.core import core
    restDomain = core.domains().restDomain()

    oauth2Service = restDomain.oauth2Service()
    oauth2CommandFactory = restDomain.oauth2CommandFactory()
    oauth2CommandBus = oauth2Service.getCommandBus()

    oauth2QueryFactory = restDomain.oauth2QueryFactory()
    oauth2QueryBus = oauth2Service.getQueryBus()

    @oauth.clientgetter
    def get_client(client_id):
        return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveClient(client_id))

    @oauth.grantgetter
    def get_grant(client_id, code):
        return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveGrant(client_id, code))

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        expires = datetime.utcnow() + timedelta(seconds=3600)
        oauth2CommandBus.handle(oauth2CommandFactory.newAppendGrant(
                client_id=client_id,
                code=code['code'],
                redirect_uri=request.redirect_uri,
                scope=' '.join(request.scopes),
                user_id=g.user.user_id,
                expires=expires
            ))

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        if access_token:
            return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveTokenByAccessToken(access_token))
        if refresh_token:
            return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveTokenByRefreshToken(refresh_token))
        return None

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        # In real project, a token is unique bound to user and client.
        # Which means, you don't need to create a token every time.
        access_token = token['access_token']
        expires = datetime.utcnow() + timedelta(seconds=int(token['expires_in']))
        scope = token['scope']
        token_type = token['token_type']

        oauth2CommandBus.handle(oauth2CommandFactory.newSetToken(request.client.client_id, request.user.user_id, access_token, expires, scope, token_type))

    #@oauth.usergetter
    #def get_user(username, password, *args, **kwargs):
    #    # This is optional, if you don't need password credential
    #    # there is no need to implement this method
    #    return User.query.filter_by(username=username).first()

    return oauth

def oauth2Routes(app, oauth):
    from strongr.core.core import core
    restDomain = core.domains().restDomain()

    oauth2Service = restDomain.oauth2Service()
    oauth2QueryFactory = restDomain.oauth2QueryFactory()
    oauth2QueryBus = oauth2Service.getQueryBus()


    @app.before_request
    def load_current_user():
        if request.values['client_id'] is not None:
            client = oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveClient(request.values['client_id']))
            if client is not None:
                g.user = client.user
                request.client = client
                request.user = g.user


    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(*args, **kwargs):
        print(request)
        if request.method == 'HEAD':
            # if HEAD is supported properly, request parameters like
            # client_id should be validated the same way as for 'GET'
            response = make_response('', 200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response

        #confirm = request.form.get('confirm', 'no')
        return True

    @app.route('/oauth/token', methods=['POST', 'GET'])
    @oauth.token_handler
    def access_token():
        from oauthlib.oauth2 import Client


        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        pass

    @oauth.invalid_response
    def require_oauth_invalid(req):
        return jsonify(message=req.error_message), 401
