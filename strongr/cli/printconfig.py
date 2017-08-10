from .wrapper import Command

class PrintConfig(Command):
    """
    Prints the config.

    print:config
    """
    def handle(self):
        config = self.getContainer().config()

        for key in config:
            print("{} = {}".format(key, config[key]))

