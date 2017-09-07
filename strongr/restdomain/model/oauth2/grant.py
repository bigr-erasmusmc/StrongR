from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from strongr.core.constants import Base


class Grant(Base):
    __tablename__ = 'grants'

    grant_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE')
    )
    user = relationship('User')

    client_id = Column(
        String(40), ForeignKey('clients.client_id', ondelete='CASCADE'),
        nullable=False,
    )
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
