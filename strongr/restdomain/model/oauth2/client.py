import strongr.core.gateways as gateways
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, func, LargeBinary, Text
from sqlalchemy.orm import relationship, synonym

from strongr.schedulerdomain.model import JobState

Base = gateways.Gateways.sqlalchemy_base()

class Client(Base):
    __tablename__ = 'oauth_client'

    name = Column(String(40))
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True, index=True, nullable=False)
    client_type = Column(String(20), default='public')

    _redirect_uris = Column(Text)
    default_scope = Column(Text, default='')

    @property
    def user(self):
        #return User.query.get(1)
        # this should link to the user table
        pass

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']
