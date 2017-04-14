from cleo import Application

from cli import DeployOpenNebulaCommand

application = Application()
application.add(DeployOpenNebulaCommand())

if __name__ == '__main__':
    application.run()
