import pytest
import sys
sys.path.append("../Event")
import dao.db as db  # noqa: E402
import dao.models as models  # noqa: E402


@pytest.fixture
def session_maker():
    db_url = "sqlite:///tests/tests.db"
    return db.SessionFactory(db_url, models.Base).get_session_maker()


@pytest.fixture
def mock_products():
    return [
        models.Product(
            name='A',
            price='2.20',
            amount=5
        ),
    ]


@pytest.fixture
def init_db(mock_products, session_maker):
    with session_maker() as session:
        session.add_all(mock_products)
        session.commit()
        yield
        session.query(models.Product).delete()
        session.commit()
