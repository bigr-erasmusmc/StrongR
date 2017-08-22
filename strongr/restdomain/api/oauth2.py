import strongr.core
from flask_oauthlib.provider import OAuth2Provider


core = strongr.core.getCore()
restDomain = core.domains().restDomain()

oauth2Service = restDomain.oauth2Service()
oauth2CommandFactory = restDomain.oauth2CommandFactory()
oauth2CommandBus = oauth2Service.getCommandBus()

oauth2QueryFactory = restDomain.oauth2QueryFactory()
oauth2QueryBus = oauth2Service.getQueryBus()

def bind_oauth2(app):
    oauth = OAuth2Provider(app)

    @oauth.clientgetter
    def get_client(client_id):
        return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveClient(client_id))

    @oauth.grantgetter
    def get_grant(client_id, code):
        return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveGrant(client_id, code))

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        if access_token:
            return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveTokenByAccessToken(access_token))
        if refresh_token:
            return oauth2QueryBus.handle(oauth2QueryFactory.newRetrieveTokenByRefreshToken(refresh_token))
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        expires = datetime.utcnow() + timedelta(seconds=600)
        oauth2CommandBus.handle(oauth2CommandFactory.newAppendGrant(
                client_id=client_id,
                code=code['code'],
                redirect_uri=request.redirect_uri,
                scope=' '.join(request.scopes),
                user_id=g.user.id,
                expires=expires
            ))

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        # In real project, a token is unique bound to user and client.
        # Which means, you don't need to create a token every time.
        tok = Token(**token)
        tok.user_id = request.user.id
        tok.client_id = request.client.client_id
        db.session.add(tok)
        db.session.commit()

    #@oauth.usergetter
    #def get_user(username, password, *args, **kwargs):
    #    # This is optional, if you don't need password credential
    #    # there is no need to implement this method
    #    return User.query.filter_by(username=username).first()

    return oauth

def oauth2Routes(app):
    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(*args, **kwargs):
        # NOTICE: for real project, you need to require login
        if request.method == 'GET':
            # render a page for user to confirm the authorization
            return render_template('confirm.html')

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
        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        pass

    @oauth.invalid_response
    def require_oauth_invalid(req):
        return jsonify(message=req.error_message), 401
