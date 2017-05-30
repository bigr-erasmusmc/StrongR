from strongr.clouddomain.query import ListDeployedVms

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    def newListDeployedVmsCommand(self):
        """ Generates a new ListDeployedVms query

        :returns: A ListDeployedVms query object
        :rtype: ListDeployedVms
        """
        return ListDeployedVms()

