from .wrapper import Command
import json

class PrintConfig(Command):
    """
    Prints the config.

    print:config
    """
    def handle(self):
        config = self.getContainer().config().as_dict()
        del config['internal']
        print(json.dumps(config, indent=2, sort_keys=True))
