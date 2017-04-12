from abc import ABCMeta, abstractmethod



class BaseCloudService():
    __metaclass__ = ABCMeta
    handlers = {}

    def __init__(self):
        self.setup()

    @abstractmethod
    def setup(self):
        return

    def injectHandler(self, handler, command):
        # TODO: do propper type checking
        self.handlers[handler] = command

    def injectHandlers(self, handlers):
        for handler in handlers:
            self.injectHandler(handler, handlers[handler])
