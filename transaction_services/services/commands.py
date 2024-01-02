from sqlalchemy import orm
import sys
sys.path.append('../transaction_services')

import models.account as bank_account


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
        with self.__session_maker() as session:
            return session.query(bank_account.BankAccountRead)\
                .filter(bank_account.BankAccountRead.code ==
                        self.__code)\
                .filter(bank_account.BankAccountRead.frozen == False)\
                .first()


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
                .filter(bank_account.BankAccountWrite.frozen == False)\
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
                .filter(bank_account.BankAccountWrite.frozen == False)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance -
                     self.__amount}
                )
            session.commit()


class Transfer(BaseCommand):
    def __init__(self,
                 session_maker: orm.sessionmaker[orm.Session],
                 code_from: str,
                 code_to: str,
                 amount: int) -> None:
        self.__session_maker = session_maker
        self.__code_from = code_from
        self.__code_to = code_to
        self.__amount = amount

    def execute(self, **args):
        with self.__session_maker() as session:
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.__code_from)\
                .filter(bank_account.BankAccountWrite.frozen == False)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance -
                     self.__amount}
                )
            session.query(bank_account.BankAccountWrite)\
                .filter(bank_account.BankAccountWrite.code ==
                        self.__code_to)\
                .filter(bank_account.BankAccountWrite.frozen == False)\
                .update(
                    {"balance": bank_account.BankAccountWrite.balance +
                     self.__amount}
                )
            session.commit()
