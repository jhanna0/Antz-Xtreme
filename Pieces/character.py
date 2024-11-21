from typing import Tuple, List
from Inventory.inventory import Inventory, Item
from Pieces.piece import Piece
from Pieces.source import Source
from Pieces.machine import Machine

class Character(Piece):
    def __init__(self, name: str, location: Tuple[int, int], symbol: str):
        super().__init__(location, symbol)
        self.inventory = Inventory()
        self.name = name

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

    def interact_with_sources(self, source: Source):
        item = source.take()
        if item:
            self.add_to_inventory(item)

    def interact_with_machine(self, machine: Machine):
        item = source.take()
        if item:
            self.add_to_inventory(item)

    # # can probably make this better and merged with NPC interaction logic
    # # this is so bad how NPC manager is cyclically referenced.. fix. probably outside of loop
    # def calculate_interactions(self, sources: SourceManager, machines: MachineManager):
    #     for source in sources.get_piece_array():
    #         if self.get_location() == source.get_location():
    #             item = source.take()
    #             if item:
    #                 self.add_to_inventory(item)
    #                 return

    #     for machine in machines.get_piece_array():
    #         if self.get_location() == machine.get_location():
    #             if self.any_in_inventory():
    #                 item = self.get_inventory().pop()
    #                 self.add_money(machine.convert(item))
    #                 BroadCast().announce(f"You sold {item.get_symbol()} for ${item.get_worth()}")
    #                 return