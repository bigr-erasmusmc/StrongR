import os

class RequestScheduledTasksHandler:
    def __call__(self, query):
        if not os.path.isdir('/tmp/strongr'):
            os.mkdir('/tmp/strongr')

        files = os.listdir('/tmp/strongr/')
        for file in files:
            print(os.path.isfile('/tmp/strongr/' + file))

        tasks = [f for f in os.listdir('/tmp/strongr/') if os.path.isfile('/tmp/strongr/' + f)].sort()
        print(tasks)
        return tasks
