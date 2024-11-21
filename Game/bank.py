class Bank:
    def __init__(self):
        self.money = 0  # Shared pool of money for the player and NPCs

    def get_money(self) -> int:
        return self.money

    def add_money(self, amount: int) -> None:
        if amount > 0:
            self.money += amount
    
    def enough_money(self, amount: int) -> bool:
        if self.money >= amount:
            return True
        return False

    def remove_money(self, amount: int) -> None:
        if amount > 0 and self.money >= amount:
            self.money -= amount

