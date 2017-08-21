from strongr.restdomain.query.wsgi import RetrieveBlueprints
#from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a rest querybus. """
    def newRetrieveBlueprints(self):
        """ Generates a new RetrieveBlueprints query

        :returns: A RetrieveBlueprints query object
        :rtype: RetrieveBlueprints
        """
        return RetrieveBlueprints()
