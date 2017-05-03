from abc import ABCMeta, abstractmethod

from strongr import core

class CallableCommandHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, command):
        pass

    def executeAndPublishDomainEvent(self, event, callable, **kwargs):
        callable(*kwargs)
        self.publishDomainEvent(event)

    def publishDomainEvent(self, event):
        core.Core.domainEventsPublisher().publish(event)
