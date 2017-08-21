from .wrapper import Command
from flask import Flask

class RunRestServerCommand(Command):
    """
    Runs the strongr REST server that sits between FASTR and STRONGR

    restdomain:startserver
        {--host=127.0.0.1 : The ip adress to listen on, can also be set trough config key 'restserver.host'}
        {--p|port=8080 : The port to listen on, can also be set trough config key 'restserver.port'}
        {--d|debug : use Flask debug server instead of Gunicorn, can also be set trough config key 'restserver.debug'}
    """
    def handle(self):
        config = self.getContainer().config()

        if 'restserver.host' in config:
            host = config['restserver.host']
        else:
            host = self.option('host')

        if 'restserver.port' in config:
            port = int(config['restserver.port'])
        else:
            port = int(self.option('port'))

        if 'restserver.debug' in config:
            debug = self._castToBool(config['restserver.debug'])
        else:
            debug = self.option('debug')

        self.info("Starting server on {}:{} using {}".format(host, port, ('Flask' if debug else 'Gunicorn')))

        domain = self.getDomains().restDomain()
        wsgiQueryFactory = domain.wsgiQueryFactory()
        wsgiQueryBus = domain.wsgiService().getQueryBus()

        blueprints = wsgiQueryBus.handle(wsgiQueryFactory.newRetrieveBlueprints())


        app = Flask(__name__)

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

        if debug:
            app.run(debug=True, host=host, port=port)
        else:
            from gunicorn.app.base import BaseApplication

            # put WSGIServer class here for now
            # this should be refactored later
            class WSGIServer(BaseApplication):
                def __init__(self, app):
                    self.application = app
                    super(WSGIServer, self).__init__("%(prog)s [OPTIONS]")

                def load_config(self):
                    self.cfg.set('bind', '{}:{}'.format(host, port))
                    for key in config:
                        if key.startswith('gunicorn.'):
                            self.cfg.set(key[9:], config[key])

                def load(self):
                    return self.application
            WSGIServer(app).run()

