import enum
from sqlalchemy import orm
import services.commands as commands


class TransactionType(enum.Enum):
    CHECK_BALANCE = 'check_balance'


class TransactionWorker:
    def __init__(self, state: TransactionType,
                 session_maker: orm.sessionmaker[orm.Session],
                 owner: str) -> None:
        self.__state = state
        self.__session_maker = session_maker
        self.__owner = owner

    def execute(self):
        if self.__state == TransactionType.CHECK_BALANCE:
            return commands.CheckBalance(self.__session_maker)\
                .execute(self.__owner)
        return
