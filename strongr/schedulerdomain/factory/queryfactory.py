from strongr.schedulerdomain.query import RequestScheduledTasks, RequestTaskInfo, FindNodeWithAvailableResources

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a scheduler querybus. """
    def newFindNodeWithAvailableResources(self, cores, ram):
        """ Generates a new FindNodeWithAvailableResources query

        :param cores: the amount of cores needed to complete the task
        :type cores: int
        :param ram: the amount of ram needed to complete the task in GiB
        :type ram: int

        :returns: A FindNodeWithAvailableResources query object
        :rtype: FindNodeWithAvailableResources
        """
        return FindNodeWithAvailableResources(cores=cores, ram=ram)

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
