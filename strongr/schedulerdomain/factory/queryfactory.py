from strongr.schedulerdomain.query import RequestScheduledJobs, RequestFinishedJobs, RequestJobInfo, FindNodeWithAvailableResources, RequestResourcesRequired

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a scheduler querybus. """

    def newRequestResourcesRequired(self):
        """ Generates a new RequestResourcesRequired query
        :returns: A RequestResourcesRequired query object
        :rtype: RequestResourcesRequired
        """
        return RequestResourcesRequired()

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

    def newRequestScheduledJobs(self):
        """ Generates a new RequestScheduledJobs query

        :returns: A RequestScheduledJobs query object
        :rtype: RequestScheduledJobs
        """
        return RequestScheduledJobs()

    def newRequestFinishedJobs(self):
        """ Generates a new RequestFinishedJobs query

        :returns: A RequestFinishedJobs query object
        :rtype: RequestFinishedJobs
        """
        return RequestFinishedJobs()

    def newRequestTaskInfo(self, taskid):
        """ Generates a new RequestTaskInfo query

        :param taskid: the taskid
        :type taskid: string

        :returns: A RequestTaskInfo query object
        :rtype: RequestJobInfo
        """
        return RequestJobInfo(taskid)
