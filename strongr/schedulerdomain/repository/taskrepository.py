from strongr import core

class TaskRepository:
    _listKey = 'task.list'

    @property
    def _store(self):
        return core.Core.keyValueStore()

    def loadTasks(self):
        return self._store.get(self._listKey)

    def updateTasks(self, tasks):
        self._store.set(_listKey, tasks)

    def storeTask(self, task):
        if not self._store.exists(self._listKey):
            self._store.set(_listKey, [task])
        else:
            taskList = self._store.get(_listKey)
            taskList.append(task)
            self._store.set(_listKey, taskList)
