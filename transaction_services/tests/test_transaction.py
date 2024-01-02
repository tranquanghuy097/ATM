import sys
sys.path.append('../transaction_services')

import models.account as bank_account
import services.controller as controller
import services.commands as commands


def test_check_balance(setup_teardown_read,
                       mock_account_read,
                       session_maker):
    expected = mock_account_read[0]
    command = commands.CheckBalance(
        session_maker=session_maker,
        code=expected.code
    )
    result = controller.TransactionController(
        command=command
    ).execute()
    assert result == expected


def test_check_balance_not_found(setup_teardown_read,
                                 session_maker):
    command = commands.CheckBalance(
        session_maker=session_maker,
        code="00000000"
    )
    result = controller.TransactionController(
        command=command
    ).execute()
    assert result == None


def test_deposit_money(setup_teardown_write,
                       mock_account_write,
                       session_maker):
    original_balance = mock_account_write[0].balance
    command = commands.Deposit(
        session_maker=session_maker,
        code=mock_account_write[0].code,
        amount=100
    )
    controller.TransactionController(
        command=command
    ).execute()
    with session_maker() as session:
        result = session.query(bank_account.BankAccountWrite)\
                    .filter(bank_account.BankAccountWrite.code ==
                            mock_account_write[0].code)\
                    .first()
        assert result.balance - original_balance == 100


def test_withdraw_money(setup_teardown_write,
                        mock_account_write,
                        session_maker):
    original_balance = mock_account_write[0].balance
    command = commands.Withdraw(
        session_maker=session_maker,
        code=mock_account_write[0].code,
        amount=100
    )
    controller.TransactionController(
        command=command
    ).execute()
    with session_maker() as session:
        result = session.query(bank_account.BankAccountWrite)\
                    .filter(bank_account.BankAccountWrite.code ==
                            mock_account_write[0].code)\
                    .first()
        assert original_balance - result.balance == 100


def test_transfer_money(setup_teardown_write,
                        mock_account_write,
                        session_maker):
    original_balance_from = mock_account_write[0].balance
    original_balance_to = mock_account_write[1].balance
    command = commands.Transfer(
        session_maker=session_maker,
        code_from=mock_account_write[0].code,
        code_to=mock_account_write[1].code,
        amount=100
    )
    controller.TransactionController(
        command=command
    ).execute()
    with session_maker() as session:
        result = session.query(bank_account.BankAccountWrite)\
                    .filter(bank_account.BankAccountWrite.code ==
                            mock_account_write[0].code)\
                    .first()
        assert original_balance_from - result.balance == 100
        result = session.query(bank_account.BankAccountWrite)\
                        .filter(bank_account.BankAccountWrite.code ==
                                mock_account_write[1].code)\
                        .first()
        assert result.balance - original_balance_to == 100
