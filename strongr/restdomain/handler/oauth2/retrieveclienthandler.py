from sqlalchemy.orm import Session
from strongr.restdomain.model.oauth2 import Client

class RetrieveClientHandler:
    def __call__(self, query):
        from strongr.core.core import core
        db = core.db()
        session = Session(db)
        client = session.query(Client).filter_by(client_id=query.client_id).first()
        session.commit()
        return client
