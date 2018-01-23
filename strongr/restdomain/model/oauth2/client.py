from sqlalchemy.orm import relationship

import strongr.core.gateways as gateways
from sqlalchemy import Column, ForeignKey, Integer

from authlib.flask.oauth2.sqla import OAuth2ClientMixin

Base = gateways.Gateways.sqlalchemy_base()

class Client(Base, OAuth2ClientMixin):
    __tablename__ = 'oauth_client'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')
