import os

class RequestScheduledTasksHandler:
    def __call__(self, query):
        if not os.path.isdir('/tmp/strongr'):
            os.mkdir('/tmp/strongr')

        return [f for f in os.listdir('/tmp/strongr/') if os.path.isfile('/tmp/strongr/' + f)]