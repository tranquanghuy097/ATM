import sqlalchemy as sql
from sqlalchemy import orm
import uuid

import models.base as base
import models.guid as guid


class BankAccountRead(base.Base):
    __tablename__ = 'bank_account_read'

    id: orm.Mapped[str] = orm.mapped_column(guid.GUID,
                                            primary_key=True,
                                            default=uuid.uuid4)
    owner: orm.Mapped[str] = orm.mapped_column(sql.String,
                                               nullable=False)
    balance: orm.Mapped[int] = orm.mapped_column(sql.Integer,
                                                 default=0)
    frozen: orm.Mapped[bool] = orm.mapped_column(sql.Boolean,
                                                 default=False)

    def __repr__(self) -> str:
        return "{} - {}".format(self.id, self.owner)


class BankAccountWrite(base.Base):
    __tablename__ = 'bank_account_write'

    id: orm.Mapped[str] = orm.mapped_column(guid.GUID,
                                            primary_key=True,
                                            default=uuid.uuid4)
    owner: orm.Mapped[str] = orm.mapped_column(sql.String,
                                               nullable=False,
                                               unique=True)
    balance: orm.Mapped[int] = orm.mapped_column(sql.Integer,
                                                 default=0)
    frozen: orm.Mapped[bool] = orm.mapped_column(sql.Boolean,
                                                 default=False)

    def __repr__(self) -> str:
        return "{} - {}".format(self.id, self.owner)
