import enum
from sqlalchemy import orm
import dao.models as models


class State(enum.Enum):
    CHECK_PRODUCTS = 'check_products'
    GET_PRODUCTS = 'get_products'
    DELIVER_PRODUCTS = 'deliver_products'


class Consumer():
    def __init__(self, state: State,
                 session_maker: orm.sessionmaker[orm.Session],
                 products: dict[str, int]) -> None:
        self.state = state
        self.session_maker = session_maker
        self.products = products

    def execute(self):
        if self.state == State.CHECK_PRODUCTS:
            return self.check_products()
        elif self.state == State.GET_PRODUCTS:
            return self.get_products()
        elif self.state == State.DELIVER_PRODUCTS:
            return self.deliver_products()
        return False

    def check_products(self) -> bool:
        product_name = [key for key in self.products]
        with self.session_maker() as session:
            result = session.query(models.Product)\
                .filter(models.Product.name.in_(product_name)).all()
            if len(result) == 0:
                return False
            for product in result:
                if product.amount < self.products[product.name]:
                    return False
            return True

    def get_products(self) -> bool:
        product_name = [key for key in self.products]
        with self.session_maker() as session:
            result = session.query(models.Product)\
                .filter(models.Product.name.in_(product_name)).all()
            for product in result:
                product.amount -= self.products[product.name]
            session.commit()
        return True

    def deliver_products(self) -> bool:
        return True
