from cleo import Application

from cli import ConfigHelperCommand

application = Application()
application.add(ConfigHelperCommand())

if __name__ == '__main__':
    application.run()
