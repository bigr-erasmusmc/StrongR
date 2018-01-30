import dependency_injector.containers as containers
import dependency_injector.providers as providers
from flask import Flask

from authlib.flask.oauth2 import AuthorizationServer
from strongr.restdomain.api.apiv1 import blueprint as apiv1

import strongr.core

class Gateways(containers.DeclarativeContainer):
    """IoC container of gateway objects."""
    _backends = providers.Object({
    })
    _blueprints = providers.Object([apiv1])

    def _factor_app(name, blueprints):
        app = Flask(__name__)

        config = strongr.core.Core.config()
        backend = config.restdomain.backend.strip().lower()

        # the oauth2 lib can not work with templates,
        # this hack was proposed as a temp fix on the
        # libraries github. Use this for now, we
        # should refactor this later.
        # https://github.com/lepture/flask-oauthlib/issues/180
        #from strongr.restdomain.api.oauth2 import bind_oauth2
        #oauth2 = bind_oauth2(app)
        #app.oauth2 = oauth2

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

        server = AuthorizationServer(Client, app)

        if backend == 'flask':
            flask_config = config.restdomain.flask.as_dict() if hasattr(config, 'restdomain') and hasattr(config.restdomain, 'flask') else {}
            # monkey patch run method so that config is grabbed from config file
            setattr(app, '_run_original', app.run)
            app.run = lambda self=app: self._run_original(**flask_config)
            return app
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
                        self.cfg.set(key, config.restdomain.gunicorn[key])

                def load(self):
                    return self.application

            return WSGIServer(app)


    app = providers.Singleton(_factor_app, 'StrongRRestServer', _blueprints())
