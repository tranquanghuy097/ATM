from sqlalchemy import orm
from sqlalchemy import exc
import sys
sys.path.append('../transaction_services')

import models.account as bank_account  # noqa: E402


class BaseCommand():
    session_maker: orm.sessionmaker[orm.Session]

    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session]) -> None:
        self.session_maker = session_maker

    def execute(self, **args):
        pass


class CheckBalance(BaseCommand):
    def execute(self, owner: str):
        try:
            with self.session_maker() as session:
                return session.query(bank_account.BankAccountRead)\
                    .filter(bank_account.BankAccountRead.owner == owner)\
                    .first()
        except exc.NoResultFound:
            print("Account belongs to {} not found".format(owner))
            return
