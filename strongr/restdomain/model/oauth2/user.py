from sqlalchemy import Column, Integer, String

from strongr.core.constants import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, index=True, nullable=False)
