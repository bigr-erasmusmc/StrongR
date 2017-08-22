from functools import wraps
import flask

# oauth2 lib does not support blueprints so we need a hack
# https://github.com/lepture/flask-oauthlib/issues/180
def blueprint_require_oauth(*scopes):
    def wrapper(f):
        @wraps(f)
        def check_oauth(*args, **kwargs):
            return app.oauth2.require_oauth(*scopes)(f)(
                *args, **kwargs
            )

        return check_oauth
    return wrapper
