import sys
sys.path.append("../Event")
import dao.workers as workers  # noqa: E402
import dao.models as models  # noqa: E402


def test_check_products_success(init_db,
                                mock_products: list[models.Product],
                                session_maker):
    products = {x.name: x.amount for x in mock_products}
    worker = workers.Consumer(
        state=workers.State.CHECK_PRODUCTS,
        session_maker=session_maker,
        products=products
    )
    assert worker.execute() == True  # noqa: E712


def test_check_products_fail_exceed_amount(init_db,
                                           mock_products: list[models.Product],
                                           session_maker):
    products = {x.name: x.amount + 1 for x in mock_products}
    worker = workers.Consumer(
        state=workers.State.CHECK_PRODUCTS,
        session_maker=session_maker,
        products=products
    )
    assert worker.execute() == False  # noqa: E712


def test_check_products_fail_not_exist(init_db,
                                       mock_products: list[models.Product],
                                       session_maker):
    products = {"aaa": x.amount + 1 for x in mock_products}
    worker = workers.Consumer(
        state=workers.State.CHECK_PRODUCTS,
        session_maker=session_maker,
        products=products
    )
    assert worker.execute() == False  # noqa: E712


def test_get_products(init_db,
                      mock_products: list[models.Product],
                      session_maker):
    products = {x.name: 1 for x in mock_products}
    worker = workers.Consumer(
        state=workers.State.GET_PRODUCTS,
        session_maker=session_maker,
        products=products
    )
    assert worker.execute() == True  # noqa: E712
    product_name = [key for key in products]
    with session_maker() as session:
        updated_products = session.query(models.Product)\
            .filter(models.Product.name.in_(product_name)).all()
        updated_products = {x.name: x.amount for x in updated_products}
        original_products = {x.name: x.amount for x in mock_products}
        for key in original_products:
            assert original_products[key] - updated_products[key] == 1


def test_deliver_products_success(init_db,
                                  mock_products: list[models.Product],
                                  session_maker):
    products = {x.name: x.amount for x in mock_products}
    worker = workers.Consumer(
        state=workers.State.DELIVER_PRODUCTS,
        session_maker=session_maker,
        products=products
    )
    assert worker.execute() == True  # noqa: E712
