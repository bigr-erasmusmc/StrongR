from abc import ABCMeta, abstractmethod

class AbstractScaleOut(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def scalein(self):
        pass
