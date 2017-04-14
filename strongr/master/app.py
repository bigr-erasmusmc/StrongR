from cleo import Application

from cli import DeployCommand

application = Application()
application.add(DeployCommand())

if __name__ == '__main__':
    application.run()
