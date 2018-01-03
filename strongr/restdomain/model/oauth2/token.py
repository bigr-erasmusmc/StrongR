import strongr.core.gateways as gateways
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, func, LargeBinary, Text
from sqlalchemy.orm import relationship, synonym

from datetime import datetime, timedelta

from strongr.schedulerdomain.model import JobState

Base = gateways.Gateways.sqlalchemy_base()

class Token(Base):
    __tablename__ = 'oauth_token'

    id = Column(Integer, primary_key=True)
    client_id = Column(
        String(40), ForeignKey('client.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')
    client = relationship('Client')
    token_type = Column(String(40))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    expires = Column(DateTime)
    scope = Column(Text)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in', None)
        if expires_in is not None:
            self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []
