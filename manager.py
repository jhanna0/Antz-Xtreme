from typing import Dict, List

class Manager:
    def __init__(self):
        self.items: Dict[str, List] = {}

    def register(self, entity):
        symbol: str = entity.get_symbol()
        if symbol not in self.items:
            self.items[symbol] = []

        self.items[symbol].append(entity)
        # self.board.update_piece_position(self.machines) -> move to Game

    def get_items(self):
        return self.items
    
    def get_piece_array(self):
        return [item for sublist in self.items.values() for item in sublist]
