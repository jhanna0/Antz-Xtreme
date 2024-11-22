

class Bank:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.balance = 0
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

    def get_money_string(self) -> str:
        balance = self.get_money()

        if balance < 1_000:
            return f"${balance}"
        elif balance < 1_000_000:
            return f"${balance / 1_000:.1f}K"
        elif balance < 1_000_000_000:
            return f"${balance / 1_000_000:.1f}M"
        else:
            return f"${balance / 1_000_000_000:.1f}B"

# all players share the same bank.. good?
# probably not, because now multipler requires passing different bank logic to NPCs
# probably don't make a singleton
bank = Bank()
