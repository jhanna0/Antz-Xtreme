import time
from typing import Tuple
from Inventory.item import Item
from Pieces.piece import Piece
from Game.definitions import Rarity

class Source(Piece):
    def __init__(self, symbol: str, location: Tuple[int, int], creation_rate: float, worth: int, rarity: Rarity):
        super().__init__(location, symbol)
        self.capacity = 6
        self.quantity = 0
        self.creation_rate = creation_rate  # Time interval to create new items
        self.worth = worth  # Value of the source items
        self.rarity = rarity
        self.last_created_time = time.time()
        self.item = Item(symbol, worth)

    def try_to_create(self, current_time: float):
        if (current_time - self.last_created_time) > self.creation_rate and self.quantity < self.capacity:
            self.quantity += 1
            self.last_created_time = current_time

    def get_quantity(self):
        return self.quantity

    def take(self):
        if self.quantity > 0:
            self.quantity -= 1
            return self.item
        return None
