from sqlalchemy import orm
from sqlalchemy import exc
import sys
sys.path.append('../transaction_services')

import models.account as bank_account  # noqa: E402
import services.command_model as command_model  # noqa: E402


class BaseCommand():
    session_maker: orm.sessionmaker[orm.Session]
    account: command_model.AccountCommandModel

    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session],
                 account: command_model.AccountCommandModel) -> None:
        self.session_maker = session_maker
        self.account = account

    def execute(self, **args):
        pass


class CheckBalance(BaseCommand):
    def execute(self):
        try:
            with self.session_maker() as session:
                return session.query(bank_account.BankAccountRead)\
                    .filter(bank_account.BankAccountRead.code ==
                            self.account.code)\
                    .first()
        except exc.NoResultFound:
            print("Account belongs to {} not found".format(
                self.account.code))
            return


class Deposit(BaseCommand):
    def execute(self, **args):
        with self.session_maker() as session:
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.account.code)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance +
                     self.account.amount}
                )
            session.commit()


class Withdraw(BaseCommand):
    def execute(self, **args):
        with self.session_maker() as session:
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.account.code)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance -
                     self.account.amount}
                )
            session.commit()
