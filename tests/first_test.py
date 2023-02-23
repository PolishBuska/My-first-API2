import pytest
from app.calculations import BankAccount


@pytest.fixture()
def zero_bank_account():
    return BankAccount()
@pytest.fixture()
def bank_account():
    return BankAccount(100)




def test_plus(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 90

def test_bad_money_amount(zero_bank_account):
    with pytest.raises(Exception):
        zero_bank_account.withdraw(10)
@pytest.mark.parametrize("deposited,withdrew , expected", [
    (100, 50, 50),
    (100, 99, 1),
    (3, 2, 1)
])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

