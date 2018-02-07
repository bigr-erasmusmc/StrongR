from authlib.specs.rfc6749.grants import (
    ClientCredentialsGrant as _ClientCredentialsGrant
)

from strongr.core.gateways import Gateways
from strongr.restdomain.model.oauth2 import Token


class ClientCredentialsGrant(_ClientCredentialsGrant):
    def create_access_token(self, token, client):
        item = Token(
            client_id=client.client_id,
            user_id=client.user_id,
            **token
        )
        session = Gateways.sqlalchemy_session()
        session.add(item)
        session.commit()
