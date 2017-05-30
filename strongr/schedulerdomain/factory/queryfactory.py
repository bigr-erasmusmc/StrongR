from strongr.schedulerdomain.query import RequestScheduledTasks

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a scheduler querybus. """

    def newRequestScheduledTasks(self):
        """ Generates a new RequestScheduledTasks query

        :returns: A RequestScheduledTasks query object
        :rtype: RequestScheduledTasks
        """
        return RequestScheduledTasks()
