from sqlalchemy.orm import Session

from strongr.restdomain.model.oauth2 import Token

class SetTokenHandler:
    def __call__(self, command):
        from strongr.core.core import core
        db = core.db()
        session = Session(db)
        tokens = session.query(Token).filter_by(user_id=command.user_id).all()
        session.commit()
        for x in range(1,200):
            len(tokens)
        for token in tokens:
            session.delete(token)
        session.commit()

        record = Token(**command.__dict__)
        session.add(record)
        session.commit()
