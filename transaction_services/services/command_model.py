import pydantic


class AccountCommandModel(pydantic.BaseModel):
    code: str
    amount: int | None = None
    to_account: str | None = None
