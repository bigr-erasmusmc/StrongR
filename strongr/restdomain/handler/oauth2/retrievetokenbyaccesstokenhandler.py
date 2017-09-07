from sqlalchemy.orm import Session

from strongr.restdomain.model.oauth2 import Token


class RetrieveTokenByAccessTokenHandler:
    def __call__(self, query):
        from strongr.core.core import core
        db = core.db()
        session = Session(db)
        result = session.query(Token).filter_by(access_token=query.access_token).first()
        session.commit()
        return result
