from .wrapper import Command
from flask import Flask

class RunRestServerCommand(Command):
    """
    Runs the strongr REST server that sits between FASTR and STRONGR

    restdomain:startserver
    """
    def handle(self):
        config = self.getContainer().config()

        host = config.restdomain.host
        port = int(config.restdomain.port)
        backend = config.restdomain.backend.strip().lower()

        self.info("Starting server on {}:{} using {}".format(host, port, backend))

        domain = self.getDomains().restDomain()
        wsgiQueryFactory = domain.wsgiQueryFactory()
        wsgiQueryBus = domain.wsgiService().getQueryBus()

        blueprints = wsgiQueryBus.handle(wsgiQueryFactory.newRetrieveBlueprints())


        app = Flask(__name__)

        # the oauth2 lib can not work with templates,
        # this hack was proposed as a temp fix on the
        # libraries github. Use this for now, we
        # should refactor this later.
        # https://github.com/lepture/flask-oauthlib/issues/180
        from strongr.restdomain.api.oauth2 import bind_oauth2
        oauth2 = bind_oauth2(app)
        app.oauth2 = oauth2

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

        if backend == 'flask':
            app.run(**config.restdomain.flask.as_dict())
        elif backend == 'gunicorn':
            from gunicorn.app.base import BaseApplication

            # put WSGIServer class here for now
            # this should be refactored later
            class WSGIServer(BaseApplication):
                def __init__(self, app):
                    self.application = app
                    super(WSGIServer, self).__init__("%(prog)s [OPTIONS]")

                def load_config(self):
                    for key in config.restdomain.gunicorn:
                        self.cfg.set(key, config[key])

                def load(self):
                    return self.application
            WSGIServer(app).run()
