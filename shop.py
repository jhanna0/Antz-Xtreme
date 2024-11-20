class Shop():
    def __init__(self, symbol: str):
        self.purchases = 0
        self.symbol = symbol
        self.base_price = 5
        self.location = (9, 19)
    
    def get_price(self):
        return int(((self.purchases + 1) + self.base_price) ** 1.5)
    
    def get_location(self):
        return self.location

    def purchase(self):
        return True

    def get_type(self):
        return "Shop"
