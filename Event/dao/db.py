import sqlalchemy as sql
from sqlalchemy import orm


class SessionFactory():
    def __init__(self, db_url: str, base: orm.DeclarativeBase) -> None:
        self.__engine = sql.create_engine(db_url)
        base.metadata.create_all(self.__engine)

    def get_session_maker(self):
        return orm.sessionmaker(bind=self.__engine)
