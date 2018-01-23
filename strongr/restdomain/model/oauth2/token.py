import strongr.core.gateways as gateways
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from authlib.flask.oauth2.sqla import OAuth2TokenMixin


Base = gateways.Gateways.sqlalchemy_base()

class Token(Base, OAuth2TokenMixin):
    __tablename__ = 'oauth_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')
