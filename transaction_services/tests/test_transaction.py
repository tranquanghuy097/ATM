import sys
sys.path.append('../transaction_services')

import services.worker as worker   # noqa: E402


def test_check_balance(setup_teardown_read,
                       mock_account_read,
                       session_maker):
    expected = mock_account_read[0]
    result = worker.TransactionWorker(
        state=worker.TransactionType.CHECK_BALANCE,
        session_maker=session_maker,
        code=expected.code
    ).execute()
    assert result == expected
