#from strongr.schedulerdomain.repository import TaskRepository
import jsonpickle
import os
import time

class ScheduleTaskHandler:
    def __call__(self, command):
        #repository = TaskRepository()
        #repository.storeTask(command)
        if not os.path.isdir('/tmp/strongr'):
            os.mkdir('/tmp/strongr')

        serialized = jsonpickle.encode(command)
        with open("/tmp/strongr/{}.{}".format(int(time.time()), command.taskid), "w") as file:
            file.write(serialized)
