from cmndr import Middleware
from sqlalchemy.exc import SQLAlchemyError

import strongr.core.gateways
import logging


class TransactionMiddleware(Middleware):
    def execute(self, command, next_callable):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()

        try:
            ret = next_callable(command)
            session.commit()
            return ret
        except SQLAlchemyError as e:
            session.rollback()
            logging.getLogger("Transaction Middleware").warning(e)
