from typing import Tuple, List
from Inventory.inventory import Inventory, Item
from Pieces.piece import Piece
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager
from Game.bank import bank
from Game.broadcast import broadcast
from Game.definitions import Speed
from Game.tick import ticks

class Character(Piece):
    def __init__(self, name: str, location: Tuple[int, int], symbol: str, sources: SourceManager, machines: MachineManager):
        super().__init__(location, symbol)
        self.inventory = Inventory()
        self.name = name
        self.sources = sources
        self.machines = machines

        # Probably a better way to do this.. just for abilities seem too specific. When action class is introduced can make a dict there
        self.ability_cooldown = Speed.SLOW
        self.last_ability_tick = 0

    def move(self, destination: Tuple[int, int]) -> None:
        """
        Moves the character to a new location.
        """
        self.location = destination

    def add_to_inventory(self, item: Item) -> None:
        self.inventory.add_to_inventory(item)

    def get_inventory(self) -> List[Item]:
        return self.inventory.get_items()

    def any_in_inventory(self) -> bool:
        return self.inventory.is_there_anything_in_inventory()

    def inventory_full(self) -> bool:
        return self.inventory.is_inventory_full()

    def interact_with_source(self) -> None:
        """
        Checks if there's a source at the character's location and interacts with it.
        """
        if self.inventory_full():
            return
        
        source = self.sources.get_piece_at_location(self.location)
        if source:
            item = source.take()
            if item:
                self.add_to_inventory(item)

    def interact_with_machine(self) -> None:
        """
        Checks if there's a machine at the character's location and interacts with it.
        """
        machine = self.machines.get_piece_at_location(self.location)
        if machine and self.any_in_inventory():
            item = self.get_inventory().pop()
            bank.add_money(machine.convert(item))
            broadcast.announce(f"{self.name} sold {item.get_symbol()} for ${item.get_worth()}")

    def turn_sequence(self) -> None:
        """
        Handles the character's interactions with sources and machines during their turn.
        """
        self.interact_with_source()
        self.interact_with_machine()
    
    # Probably a better way to do this.. just for abilities seem too specific. When action class is introduced can make a dict there
    def set_last_ability_tick(self):
        self.last_ability_tick = ticks.get_current_tick()
    
    def can_use_ability(self) -> bool:
        diff = ticks.get_tick_difference(self.last_ability_tick) >= self.ability_cooldown.value
        if diff:
            self.set_last_ability_tick()
        return diff
