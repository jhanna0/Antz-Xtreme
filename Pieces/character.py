from typing import Tuple, List
from Inventory.inventory import Inventory, Item
from Pieces.piece import Piece
from Pieces.source import Source
from Pieces.machine import Machine
from Game.bank import Bank
from Game.broadcast import BroadCast

class Character(Piece):
    def __init__(self, name: str, location: Tuple[int, int], symbol: str, bank: Bank):
        super().__init__(location, symbol)
        self.inventory = Inventory()
        self.name = name
        self.bank = bank

    def move(self) -> None:
        raise NotImplementedError("Move not implemented for base Character class.")

    def add_to_inventory(self, item) -> None:
        self.inventory.add_to_inventory(item)

    def get_inventory(self) -> List[Item]:
        return self.inventory.get_items()

    def get_capacity(self) -> int:
        return self.inventory.get_capacity()

    def inventory_full(self) -> bool:
        return self.inventory.is_inventory_full()

    def any_in_inventory(self) -> bool:
        return self.inventory.is_there_anything_in_inventory()

    # could return bool?
    def interact_with_source(self, source: Source) -> None:
        item = source.take()
        if item:
            self.add_to_inventory(item)
            
    # could return bool?
    def interact_with_machine(self, machine: Machine) -> None:
        if self.any_in_inventory():
            item = self.get_inventory().pop()
            self.bank.add_money(machine.convert(item))
            broadcast.announce(f"{self.name} sold {item.get_symbol()} for ${item.get_worth()}")
