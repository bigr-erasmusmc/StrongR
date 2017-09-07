from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from uuid import uuid4

from strongr.restdomain.model.oauth2.user import User

from strongr.core.constants import Base

def _generate_client_id(self):
    return str(uuid4()).replace('-', '')

class Client(Base):
    __tablename__ = 'clients'

    # id = Column(Integer, primary_key=True)
    # human readable name
    name = Column(String(40))
    client_id = Column(String(32), primary_key=True, default=_generate_client_id)
    client_secret = Column(String(55), unique=True, index=True,
                              nullable=False)
    client_type = Column(String(20), default='public')
    _redirect_uris = Column(Text)
    default_scope = Column(Text, default='email address')

    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE')
    )
    user = relationship('User')

    @property
    def user(self):
        from strongr.core.core import core
        db = core.db()
        session = Session(db)
        user = session.query(User).filter_by(user_id=self.user_id).first()
        session.commit()
        return user

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
        # 'authorization_code', 'password'
        return ['client_credentials', 'refresh_token']
