import jsonpickle
import os
import filelock

class ScheduleTaskHandler:
    def __call__(self, command):
        if not os.path.isdir('/tmp/strongr'):
            os.mkdir('/tmp/strongr')

        serialized = jsonpickle.encode(command)

        lock = filelock.FileLock("strongr-tasks-lock")
        with lock.acquire(timeout = 10):
            with open("/tmp/strongr/{}".format(command.taskid), "w") as file:
                file.write(serialized)
