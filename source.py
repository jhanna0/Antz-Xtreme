import time
from typing import Tuple
from item import Item

class Source:
    def __init__(self, symbol: str, location: Tuple[int, int], creation_rate: float, worth: int):
        self.symbol = symbol
        self.capacity = 6
        self.quantity = 0
        self.creation_rate = creation_rate  # Time interval to create new items
        self.worth = worth  # Value of the source items
        self.location = location
        self.last_created_time = time.time()
        self.item = Item(symbol, worth)

    def try_to_create(self, current_time: float):
        """Create new items if enough time has passed since the last creation."""
        if (current_time - self.last_created_time) > self.creation_rate and self.quantity < self.capacity:
            self.quantity += 1
            self.last_created_time = current_time

    def get_location(self):
        return self.location

    def get_type(self):
        return "Source"

    def get_quantity(self):
        return self.quantity

    def take(self):
        if self.quantity > 0:
            self.quantity -= 1
            return self.item
        return None
    
    def get_symbol(self):
        return self.symbol
