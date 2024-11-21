from typing import Tuple

from Inventory.item import Item
from Pieces.piece import Piece
from Game.definitions import Rarity
from Game.tick import ticks

class Source(Piece):
    def __init__(self, symbol: str, location: Tuple[int, int], creation_rate: float, worth: int, rarity: Rarity):
        super().__init__(location, symbol)
        self.capacity = 6
        self.quantity = 0
        self.last_grow = 0
        self.creation_rate = creation_rate  # Time interval to create new items
        self.worth = worth  # Value of the source items
        self.rarity = rarity
        self.item = Item(symbol, worth)

    def grow(self):
        game_tick = ticks.get_current_tick()
        if (game_tick - self.last_grow) > self.creation_rate and self.quantity < self.capacity:
            self.last_grow = game_tick
            self.quantity += 1

    def get_quantity(self):
        return self.quantity

    def take(self):
        if self.quantity > 0:
            self.quantity -= 1
            return self.item
        return None
