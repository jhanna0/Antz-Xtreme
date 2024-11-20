class Item():
    def __init__(self, symbol: str, worth: int):
        self.symbol = symbol
        self.worth = worth

    def get_symbol(self):
        return self.symbol

    def get_worth(self):
        return self.worth
