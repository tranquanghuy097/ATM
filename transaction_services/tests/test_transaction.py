import sys
sys.path.append('../transaction_services')

import models.account as bank_account   # noqa: E402
import services.controller as controller   # noqa: E402
import services.command_model as command_model   # noqa: E402
import services.commands as commands   # noqa: E402


def test_check_balance(setup_teardown_read,
                       mock_account_read,
                       session_maker):
    expected = mock_account_read[0]
    account = command_model.AccountCommandModel(
        code=expected.code
    )
    command = commands.CheckBalance(
        session_maker=session_maker,
        account=account
    )
    result = controller.TransactionController(
        command=command
    ).execute()
    assert result == expected


def test_check_balance_not_found(setup_teardown_read,
                                 session_maker):
    account = command_model.AccountCommandModel(
        code="00000000"
    )
    command = commands.CheckBalance(
        session_maker=session_maker,
        account=account
    )
    result = controller.TransactionController(
        command=command
    ).execute()
    assert result == None   # noqa: E711


def test_deposit_money(setup_teardown_write,
                       mock_account_write,
                       session_maker):
    original_balance = mock_account_write[0].balance
    account = command_model.AccountCommandModel(
        code=mock_account_write[0].code,
        amount=100
    )
    command = commands.Deposit(
        session_maker=session_maker,
        account=account
    )
    controller.TransactionController(
        command=command
    ).execute()
    with session_maker() as session:
        result = session.query(bank_account.BankAccountWrite)\
                    .filter(bank_account.BankAccountWrite.code ==
                            account.code)\
                    .first()
        assert result.balance - original_balance == 100


def test_withdraw_money(setup_teardown_write,
                        mock_account_write,
                        session_maker):
    original_balance = mock_account_write[0].balance
    account = command_model.AccountCommandModel(
        code=mock_account_write[0].code,
        amount=100
    )
    command = commands.Withdraw(
        session_maker=session_maker,
        account=account
    )
    controller.TransactionController(
        command=command
    ).execute()
    with session_maker() as session:
        result = session.query(bank_account.BankAccountWrite)\
                    .filter(bank_account.BankAccountWrite.code ==
                            account.code)\
                    .first()
        assert original_balance - result.balance == 100
