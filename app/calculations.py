

class Insufficient(Exception):
    pass
class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance = starting_balance

    def deposit(self,amount):
        self.balance += amount

    def withdraw(self,amount):
        if amount > self.balance:
            raise Insufficient("Not enough")
        self.balance -= amount


    def collect_interest(self):
        self.balance *=1.1
