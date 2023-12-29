import sqlalchemy as sql
from sqlalchemy import orm
import uuid

import models.base as base
import models.guid as guid


class BankAccount(base.Base):
    __tablename__ = 'bank_account'

    id: orm.Mapped[str] = orm.mapped_column(guid.GUID,
                                            primary_key=True,
                                            default=uuid.uuid4)
    owner: orm.Mapped[str] = orm.mapped_column(sql.String,
                                               nullable=False)
    balance: orm.Mapped[int] = orm.mapped_column(sql.Integer,
                                                 default=0)
    frozen: orm.Mapped[bool] = orm.mapped_column(sql.Boolean,
                                                 default=False)
