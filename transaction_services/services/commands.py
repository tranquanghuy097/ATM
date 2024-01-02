from sqlalchemy import orm
from sqlalchemy import exc
import sys
sys.path.append('../transaction_services')

import models.account as bank_account  # noqa: E402


class BaseCommand():
    def execute(self, **args):
        pass


class CheckBalance(BaseCommand):
    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session],
                 code: str) -> None:
        self.__session_maker = session_maker
        self.__code = code

    def execute(self):
        try:
            with self.__session_maker() as session:
                return session.query(bank_account.BankAccountRead)\
                    .filter(bank_account.BankAccountRead.code ==
                            self.__code)\
                    .first()
        except exc.NoResultFound:
            print("Account belongs to {} not found".format(
                self.__code))
            return


class Deposit(BaseCommand):
    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session],
                 code: str,
                 amount: int) -> None:
        self.__session_maker = session_maker
        self.__code = code
        self.__amount = amount

    def execute(self, **args):
        with self.__session_maker() as session:
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.__code)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance +
                     self.__amount}
                )
            session.commit()


class Withdraw(BaseCommand):
    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session],
                 code: str,
                 amount: int) -> None:
        self.__session_maker = session_maker
        self.__code = code
        self.__amount = amount

    def execute(self, **args):
        with self.__session_maker() as session:
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.__code)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance -
                     self.__amount}
                )
            session.commit()
