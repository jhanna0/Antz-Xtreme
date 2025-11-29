from typing import Tuple, List
from Inventory.inventory import Inventory, Item
from Pieces.piece import Piece
from Game.bank import bank
from Game.broadcast import broadcast
from Game.definitions import Speed, SignalType
from Game.tick import ticks
from Game.signals import signals

class Character(Piece):
    def __init__(self, name: str, location: Tuple[int, int], symbol: str):
        super().__init__(location, symbol)
        self.inventory = Inventory()
        self.name = name
        
        # Subscribe to interaction signals
        signals.subscribe(SignalType.INTERACT_WITH_SOURCE, self._handle_source_interaction)
        signals.subscribe(SignalType.INTERACT_WITH_MACHINE, self._handle_machine_interaction)

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

    def _handle_source_interaction(self, signal):
        """
        Callback for when a source is found at the character's location.
        """
        if signal.data.get("target") != self:
            return
            
        if self.inventory_full():
            return
        
        source = signal.data.get("source")
        if source:
            item = source.take()
            if item:
                self.add_to_inventory(item)

    def _handle_machine_interaction(self, signal):
        """
        Callback for when a machine is found at the character's location.
        """
        if signal.data.get("target") != self:
            return

        machine = signal.data.get("machine")
        if machine and self.any_in_inventory():
            item = self.get_inventory().pop()
            bank.add_money(machine.convert(item))
            broadcast.announce(f"{self.name} sold {item.get_symbol()} for ${item.get_worth()}")

    def update(self) -> None:
        """
        Handles the character's interactions with sources and machines during their turn.
        """
        # Emit query for interactions at current location
        signals.emit(SignalType.INTERACTION_QUERY, {"piece": self, "location": self.location})
    
    # Probably a better way to do this.. just for abilities seem too specific. When action class is introduced can make a dict there
    def set_last_ability_tick(self):
        self.last_ability_tick = ticks.get_current_tick()
    
    def can_use_ability(self) -> bool:
        diff = ticks.get_tick_difference(self.last_ability_tick) >= self.ability_cooldown.value
        if diff:
            self.set_last_ability_tick()
        return diff
