from strongr.core.exception import IsNotCallableException

class DomainEventsPublisher:
    def __init__(self):
        self._subscribers = {}

    def unsubscribe(self, event, subscriber):
        if not callable(subscriber):
            raise IsNotCallableException()

        eventClass = event.__name__
        if eventClass not in self._subscribers:
            return

        self._subscribers[eventClass].remove(subscriber)

    def subscribe(self, event, subscriber):
        if not callable(subscriber):
            raise IsNotCallableException()

        eventClass = event.__name__
        if eventClass not in self._subscribers:
            self._subscribers[eventClass] = []

        self._subscribers[eventClass].append(subscriber)

    def publish(self, event):
        eventClass = event.__class__.__name__
        if eventClass in self._subscribers:
            for subscriber in self._subscribers[eventClass]:
                if not subscriber(eventClass):
                    # stop eventClass bubbling on false
                    return False
        return True
