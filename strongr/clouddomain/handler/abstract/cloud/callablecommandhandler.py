from abc import ABCMeta, abstractmethod
from multiprocessing import Pool

#from strongr.core import Core

class CallableCommandHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, command):
        pass

    def asyncDomainEventOnLambdaReturn(self, event, lambdaFunction, args=None):
        pool = Pool(processes=1)
        result = pool.apply_async(lambdaFunction, args, callback)
