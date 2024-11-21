from Inventory.item import Item
from typing import List

class Inventory():
    def __init__(self):
        self.items: List[Item] = []
        self.capacity: int = 6
    
    def get_items(self) -> List[Item]:
        return self.items

    def get_items_symbols(self) -> List[str]:
        return [item.get_symbol() for item in self.items]
    
    def get_capacity(self) -> int:
        return self.capacity

    def add_to_inventory(self, item: Item):
        if len(self.items) < self.capacity:
            self.items.append(item)
    
    def is_inventory_full(self) -> bool:
        return self.capacity == len(self.items)

    def is_there_anything_in_inventory(self) -> bool:
        return len(self.items) > 0
