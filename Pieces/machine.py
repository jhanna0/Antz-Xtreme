from typing import Tuple

from Inventory.item import Item
from Pieces.piece import Piece


class Machine(Piece):
    def __init__(self, symbol: str, location: Tuple[int, int] = (4, 0)): # can't make order consistent because of defaults
        super().__init__(location, symbol)
        self.efficiency = 1

    def convert(self, item: Item):
        raise NotImplementedError(f"Convert not implemented")
    
    def get_symbol(self):
        return self.symbol

class MoneyMachine(Machine):
    def __init__(self, symbol: str, location: Tuple[int, int]):
        super().__init__(symbol, location)

    def convert(self, item: Item):
        return item.get_worth()
