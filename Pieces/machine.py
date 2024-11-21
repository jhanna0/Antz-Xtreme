from Inventory.item import Item
from piece import Piece

class Machine(Piece):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.location = (4, 0)
        self.efficiency = 1  # Multiplier for conversion rates

    def convert(self, item):
        raise NotImplementedError(f"Convert not implemented")

    def get_type(self):
        return "Machine"
    
    def get_symbol(self):
        return self.symbol

class MoneyMachine(Machine):
    def __init__(self, symbol: str):
        super().__init__(symbol)

    def convert(self, item: Item):
        return item.get_worth()
