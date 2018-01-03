import strongr.core.gateways as gateways
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, func, LargeBinary, Text
from sqlalchemy.orm import relationship, synonym

from strongr.schedulerdomain.model import JobState

Base = gateways.Gateways.sqlalchemy_base()

class Grant(Base):
    __tablename__ = 'oauth_grant'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')

    client_id = Column(String(40), ForeignKey('client.client_id', ondelete='CASCADE'), nullable=False)
    client = relationship('Client')
    code = Column(String(255), index=True, nullable=False)

    redirect_uri = Column(String(255))
    scope = Column(Text)
    expires = Column(DateTime)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return None
