from sqlalchemy import Table, MetaData, Column, Integer, String, Text, DateTime, ForeignKey
from strongr.restdomain.command.oauth2 import AppendGrant

metadata = MetaData()

grant = Table('grant', metadata,
            Column('id', Integer, primary_key=True),
            Column('client_id', String(64)),
            Column('code', String(255)),
            Column('redirect_uri', String(255)),
            Column('scope', Text),
            Column('user_id', Integer),
            Column('expires', DateTime)
        )

user = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(64)),
            Column('password', String(256))
        )
