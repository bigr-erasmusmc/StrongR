from abc import ABCMeta, abstractmethod

class CallableCommandHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, command):
        pass
