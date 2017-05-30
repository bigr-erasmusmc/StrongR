from strongr.schedulerdomain.query import RequestScheduledTasks, RequestTaskInfo

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a scheduler querybus. """

    def newRequestScheduledTasks(self):
        """ Generates a new RequestScheduledTasks query

        :returns: A RequestScheduledTasks query object
        :rtype: RequestScheduledTasks
        """
        return RequestScheduledTasks()

    def newRequestTaskInfo(self, taskid):
        """ Generates a new RequestTaskInfo query

        :param taskid: the taskid
        :type taskid: string

        :returns: A RequestTaskInfo query object
        :rtype: RequestTaskInfo
        """
        return RequestTaskInfo(taskid)
