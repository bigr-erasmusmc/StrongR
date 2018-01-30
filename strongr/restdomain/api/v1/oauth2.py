from flask_restplus import Namespace

ns = Namespace('oauth', description='Operations related to oauth2 login')


@ns.route('/login')
def login():
    callback_uri = url_for('.authorize', _external=True)
    return oauth.twitter.authorize_redirect(callback_uri)

@ns.route('/authorize')
def authorize():
    token = oauth.twitter.authorize_access_token()
    # this is a pseudo method, you need to implement it yourself
    MyTokenModel.save(token)
    return redirect('/profile')
