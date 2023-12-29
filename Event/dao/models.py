import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
import uuid


class Base(orm.DeclarativeBase):
    pass


class GUID(types.TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgresql.UUID())
        else:
            return dialect.type_descriptor(types.CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class Product(Base):
    __tablename__ = 'product'
    id: orm.Mapped[str] = orm.mapped_column(GUID,
                                            primary_key=True,
                                            default=uuid.uuid4)
    name: orm.Mapped[str] = orm.mapped_column(sql.String, unique=True)
    price: orm.Mapped[float] = orm.mapped_column(sql.Float, default=0)
    amount: orm.Mapped[int] = orm.mapped_column(sql.Integer, default=0)
