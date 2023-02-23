import pytest
from app.calculations import add, multiply,subtract,divide,BankAccount

@pytest.fixture()
def zero_bank_account():
    return BankAccount()
@pytest.fixture()
def bank_account():
    return BankAccount(100)
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 100, 107),
    (123, 2, 125)
])
def test_add(num1,num2,expected): # naming of a function matters it should be test_something
    print("testing add function")
    assert add(num1, num2) == expected
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100
def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
def test_withdraw(bank_account):

    bank_account.withdraw(99)
    assert bank_account.balance == 1
def test_deposit(bank_account):
    bank_account.deposit(120)
    assert bank_account.balance == 220
def test_deposit(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6 == 110)