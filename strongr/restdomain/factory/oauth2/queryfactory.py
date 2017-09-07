from strongr.restdomain.query.oauth2 import RetrieveClient, RetrieveGrant, \
    RetrieveTokenByAccessToken, RetrieveTokenByRefreshToken, RetrieveUserByClientId

from strongr.core.exception import InvalidParameterException

class QueryFactory:
    """ This factory instantiates query objects to be sent to a rest querybus. """

    def newRetrieveUserByClientId(self, client_id):
        client_id = client_id.strip()
        if not len(client_id) > 0:
            raise InvalidParameterException('Client id is invalid')

        return RetrieveUserByClientId(client_id)

    def newRetrieveClient(self, client_id):
        """ Generates a new RetrieveClient query

        :param client_id: the client id
        :type client_id: string

        :returns: A RetrieveClient query object
        :rtype: RetrieveClient
        """
        client_id = client_id.strip()
        if not len(client_id) > 0:
            raise InvalidParameterException('Client id is invalid')

        return RetrieveClient(client_id=client_id)

    def newRetrieveGrant(self, client_id, code):
        """ Generates a new RetrieveGrant query

        :param client_id: the client id
        :type client_id: string

        :param code: the code
        :type code: string

        :returns: A RetrieveGrant query object
        :rtype: RetrieveGrant
        """
        client_id = client_id.strip()
        if not len(client_id) > 0:
            raise InvalidParameterException('Client id is invalid')

        code = code.strip()
        if not len(code) > 0:
            raise InvalidParameterException('Code is invalid')

        return RetrieveGrant(client_id=client_id, code=code)

    def newRetrieveTokenByAccessToken(self, access_token):
        """ Generates a new RetrieveTokenByAccessToken query

        :param access_token: the access token
        :type access_token: string

        :returns: A RetrieveTokenByAccessToken query object
        :rtype: RetrieveTokenByAccessToken
        """
        access_token = access_token.strip()
        if not len(access_token) > 0:
            raise InvalidParameterException('access_token is invalid')

        return RetrieveTokenByAccessToken(access_token)

    def newRetrieveTokenByRefreshToken(self, refresh_token):
        """ Generates a new RetrieveTokenByRefreshToken query

        :param refresh_token: the refresh token
        :type refresh_token: string

        :returns: A RetrieveTokenByRefreshToken query object
        :rtype: RetrieveTokenByRefreshToken
        """
        refresh_token = refresh_token.strip()
        if not len(refresh_token) > 0:
            raise InvalidParameterException('refresh_token is invalid')

        return RetrieveTokenByRefreshToken(refresh_token)
