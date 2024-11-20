import time

class Source():
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.capacity = 6
        self.quantity = 0
        self.creation_rate = 2
        self.location = (2, 5)
        self.last_created_time = time.time()
    
    def try_to_create(self, time: int):
        if (time - self.last_created_time) > self.creation_rate and self.quantity < self.capacity:
            self.quantity += 1
            self.last_created_time = time
    
    def get_location(self):
        return self.location

    def get_type(self):
        return "Source"

    def get_quantity(self):
        return self.quantity

    def take(self):
        if self.quantity > 0:
            self.quantity -= 1
            return self.symbol
        
        return None
