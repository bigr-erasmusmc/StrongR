from strongr.restdomain.command.oauth2 import AppendGrant, SetToken, BindOauth2ToApp
from strongr.core.exception import InvalidParameterException
from datetime import datetime

class CommandFactory:
    """ This factory instantiates command objects to be sent to a rest commandbus. """

    def newBindOauth2ToApp(self, app):
        # we should probably check if app is really a flask app here ....
        return BindOauth2ToApp(app)

    def newSetToken(self, client_id, user_id, access_token, expires, scope, token_type):
        client_id = client_id.strip()
        if not len(client_id) > 0:
            raise InvalidParameterException('Client id is invalid')

        if not user_id > 0:
             raise InvalidParameterException('User id is invalid')

        access_token = access_token.strip()
        if not len(access_token) > 0:
            raise InvalidParameterException('access_token is invalid')

        if expires <= datetime.utcnow():
            raise InvalidParameterException('expires is invalid')

        scope = scope.strip()
        if not len(scope) > 0:
            raise InvalidParameterException('scope is invalid')

        token_type = token_type.strip()
        if not len(token_type) > 0:
            raise InvalidParameterException('token_type is invalid')

        return SetToken(user_id, client_id, access_token, expires, scope, token_type)

    def newAppendGrant(self, client_id, code, redirect_uri, scope, user_id, expires):
        """ Generates a new AppendGrant command

        :param client_id: the client id
        :type client_id: string

        :param code: the code
        :type code: string

        :param redirect_uri: the redirect uri
        :type redirect_uri: string

        :param scope: the scope
        :type scope: string

        :param user_id: the user_id
        :type user_id: string

        :param expires: when should the grant expire?
        :type expires: int

        :returns: An AppendGrant command object
        :rtype: AppendGrant
        """
        client_id = client_id.strip()
        if not len(client_id) > 0:
            raise InvalidParameterException('Client id is invalid')

        code = code.strip()
        if not len(code) > 0:
            raise InvalidParameterException('Code is invalid')

        redirect_uri = redirect_uri.strip()
        if not len(redirect_uri) > 0:
            raise InvalidParameterException('Redirect uri is invalid')

        scope = scope.strip()
        if not len(scope) > 0:
            raise InvalidParameterException('Scope is invalid')

        user_id = user_id.strip()
        if not len(user_id) > 0:
            raise InvalidParameterException('User id is invalid')


        if not expires >= 0:
            raise InvalidParameterException('Expires is invalid')

        return AppendGrant(client_id, code, redirect_uri, scope, user_id, expires)
