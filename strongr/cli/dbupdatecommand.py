from strongr.restdomain.model.oauth2 import Grant
from .wrapper import Command
from sqlalchemy.orm import Session

from strongr.core.constants import Base

class DbUpdateCommand(Command):
    """
    Updates the database!

    db:update
    """
    def handle(self):
        schemas = self.getDomains().restDomain().oauth2Service().getSchemas()

        if self.getContainer().config()['database.loadtestdata']:
            Base.metadata.drop_all(self.getContainer().db())

        Base.metadata.create_all(self.getContainer().db())

        if self.getContainer().config()['database.loadtestdata']:
            from strongr.restdomain.model.oauth2 import Client, User
            client = Client()
            user = User()
            client.client_secret = 'supersecret'
            client.name = 'testclient'
            client._redirect_uris = '/authorized'
            user.username = 'testuser'

            db = self.getContainer().db()
            session = Session(db)
            session.add(user)
            session.commit()
            self.info('New user with id {} created'.format(user.user_id))

            client.user_id = user.user_id
            session.add(client)
            session.commit()
            self.info('New client with id {} created'.format(client.client_id))

            from datetime import datetime, timedelta
            grant = Grant(
                user_id=user.user_id, client_id='public',
                code='12345', scope='email',
                expires=datetime.utcnow() + timedelta(seconds=100)
            )
            session.add(grant)
            session.commit()

