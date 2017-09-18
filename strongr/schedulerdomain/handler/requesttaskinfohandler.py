import os
import jsonpickle
import filelock

class RequestTaskInfoHandler:
    def __call__(self, query):
        lock = filelock.FileLock("strongr-tasks-lock")
        with lock.acquire(timeout = 10):
            if not os.path.isfile('/tmp/strongr/' + query.taskid):
                return None # do nothing for now TODO: throw a propper exception

            with open("/tmp/strongr/{}".format(query.taskid), "r") as file:
                scheduledTask = jsonpickle.decode(file.read())

        return scheduledTask.__dict__

