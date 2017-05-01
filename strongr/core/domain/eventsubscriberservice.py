from strongr.core.exception import IsNotCallableException

class EventSubscriberService:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event, subscriber):
        if not callable(subscriber):
            raise IsNotCallableException()

        if event not in self._subscribers:
            self._subscribers[event] = []

        self._subscribers.append(subscriber)

    def publish(self, event):
        if event in self._subscribers:
            for subscriber in self._subscribers[event]:
                if not subscriber(event):
                    # stop event bubbling on false
                    return False
        return True
