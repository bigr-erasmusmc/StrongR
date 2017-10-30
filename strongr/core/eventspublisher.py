from strongr.core.exception import IsNotCallableException

import logging

class EventsPublisher:
    def __init__(self):
        self._subscribers = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    def unsubscribe(self, event, subscriber):
        if not callable(subscriber):
            raise IsNotCallableException()

        eventClass = event.__name__
        if eventClass not in self._subscribers:
            return

        self._subscribers[eventClass].remove(subscriber)

    def subscribe(self, event, callable_subscriber):
        eventClass = event.__name__
        if eventClass not in self._subscribers:
            self._subscribers[eventClass] = []

        if not callable(callable_subscriber):
            raise IsNotCallableException()

        self._subscribers[eventClass].append(callable_subscriber)

    def publish(self, event):
        event_class = event.__class__.__name__
        self._logger.debug('publishing event {} {}'.format(event_class, event))
        if event_class in self._subscribers:
            for subscriber in self._subscribers[event_class]:
                if not subscriber(event_class):
                    # stop eventClass bubbling on false
                    return False
        return True
