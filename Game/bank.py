from typing import Optional

class Bank:
    _instance: Optional["Bank"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.balance = 100
        return cls._instance

    def get_money(self) -> int:
        return self.balance

    def add_money(self, amount: int) -> None:
        if amount > 0:
            self.balance += amount
    
    def enough_money(self, amount: int) -> bool:
        if self.balance >= amount:
            return True
        return False

    def remove_money(self, amount: int) -> None:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount

# all players share the same bank.. good?
bank = Bank()
