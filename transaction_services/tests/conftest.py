import pytest
from sqlalchemy import orm
import sys
sys.path.append('../transaction_services')

import models.account as bank_account  # noqa: E402
import models.base as base   # noqa: E402
import db.db_factory as db  # noqa: E402


@pytest.fixture
def session_maker():
    db_url = "sqlite:///tests/test.db"
    return db.SessionMakerFactory(db_url, base.Base).get_session_maker()


@pytest.fixture
def mock_account_read():
    return [
        bank_account.BankAccountRead(
            code='1234567'
        ),
    ]


@pytest.fixture
def setup_teardown_read(session_maker: orm.sessionmaker[orm.Session],
                        mock_account_read: list[bank_account.BankAccountRead]):
    with session_maker() as session:
        session.add_all(mock_account_read)
        session.commit()
        yield
        session.query(bank_account.BankAccountRead).delete()
        session.commit()


@pytest.fixture
def mock_account_write():
    return [
        bank_account.BankAccountWrite(
            code='1234567',
            balance=500
        ),
        bank_account.BankAccountWrite(
            code='8765432',
            balance=100
        ),
    ]


@pytest.fixture
def setup_teardown_write(session_maker: orm.sessionmaker[orm.Session],
                         mock_account_write: list[bank_account.BankAccountWrite]):   # noqa: E501
    with session_maker() as session:
        session.add_all(mock_account_write)
        session.commit()
        yield
        session.query(bank_account.BankAccountWrite).delete()
        session.commit()
