from cleo import Application

from cli import DeploySingleCommand

application = Application()
application.add(DeploySingleCommand())

if __name__ == '__main__':
    application.run()
