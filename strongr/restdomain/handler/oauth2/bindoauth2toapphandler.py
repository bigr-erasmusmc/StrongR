import strongr.restdomain.api.oauth2 as oauth2

class BindOauth2ToAppHandler:
    def __call__(self, command):
        # the oauth2 lib can not work with templates,
        # this hack was proposed as a temp fix on the
        # libraries github. Use this for now, we
        # should refactor this later.
        # https://github.com/lepture/flask-oauthlib/issues/180
        app = command.app
        oauth = oauth2.bind_oauth2(app)
        app.oauth2 = oauth
        oauth2.oauth2Routes(command.app, oauth)

        import logging
        import sys
        log = logging.getLogger('oauthlib')
        log.addHandler(logging.StreamHandler(sys.stdout))
        log.setLevel(logging.DEBUG)

