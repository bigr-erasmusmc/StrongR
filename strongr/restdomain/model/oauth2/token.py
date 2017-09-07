from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from strongr.core.constants import Base


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    client_id = Column(
        String(40), ForeignKey('clients.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE')
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
