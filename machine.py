class Machine():
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.location = (4, 0)

    def convert(self, item):
        raise NotImplementedError(f"Convert not implemented")

    def get_location(self):
        return self.location

    def get_type(self):
        return "Machine"

class MoneyMachine(Machine):
    def __init__(self, symbol: str):
        super().__init__(symbol)

    def convert(self, item):
        if item == "@":
            return 8
