import sqlalchemy as sql
from sqlalchemy import orm


class SessionMakerFactory():
    def __init__(self, db_url: str) -> None:
        engine = sql.create_engine(db_url)
        self.__session_maker = orm.sessionmaker(bind=engine)

    def get_session_maker(self):
        return self.__session_maker
