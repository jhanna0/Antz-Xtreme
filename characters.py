from enum import Enum
from typing import Tuple, Dict, List, Set
from source import Source
from source_manager import SourceManager
from machine_manager import MachineManager
from shop_manager import ShopManager
from machine import Machine
from shop import Shop
from controller import Direction
from inventory import Inventory
from broadcast import BroadCast

class Type(Enum):
    Player = "Player"
    Robot = "Robot"
    NPC = "NPC"

class State(Enum):
    Idle = "Idle"
    Collect = "Collect"
    Sell = "Sell"

class Character:
    def __init__(
        self, 
        character_type: Type, 
        name: str, 
        symbol: str, 
        location: Tuple[int, int] = (0, 0)
    ):
        self.character_type = character_type
        self.symbol = symbol
        self.name = name
        self.location = location
        self.inventory = Inventory()

    def get_location(self) -> Tuple[int, int]:
        return self.location

    def set_location(self, location: Tuple[int, int]):
        self.location = location

    def move(self):
        raise NotImplementedError("Move not implemented for base Character class.")

    def add_to_inventory(self, item):
        self.inventory.add_to_inventory(item)

    def get_inventory(self) -> List:
        return self.inventory.get_items()

    def get_capacity(self) -> int:
        return self.inventory.get_capacity()

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> str:
        return self.character_type.value

    def inventory_full(self) -> bool:
        return self.inventory.is_inventory_full()

    def any_in_inventory(self) -> bool:
        return self.inventory.is_there_anything_in_inventory()
    
class NPC(Character):
    def __init__(
        self, 
        character_type: Type, 
        name: str, 
        symbol: str = "*", 
        location: Tuple[int, int] = (9, 18), 
        state: State = State.Idle
    ):
        super().__init__(character_type, name, symbol, location)
        self.destination: Tuple[int, int] = (0, 0)
        self.inventory_types: Set[str] = set()
        self.state = state

    def move(self) -> Tuple[int, int]:
        """Move the NPC one step toward its destination."""
        x, y = self.location
        dest_x, dest_y = self.destination

        # Determine direction of movement
        dx = dest_x - x
        dy = dest_y - y

        # Move vertically first, then horizontally
        if dx != 0:
            x += 1 if dx > 0 else -1
        elif dy != 0:
            y += 1 if dy > 0 else -1

        # Update location
        self.location = (x, y)
        return self.location

    def set_destination(self, destination: Tuple[int, int]):
        self.destination = destination

    def get_destination(self) -> Tuple[int, int]:
        return self.destination

    def add_inventory_type(self, item_type: str):
        self.inventory_types.add(item_type)

    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types

    def at_destination(self) -> bool:
        return self.destination == self.location

    def set_state(self, state: State):
        self.state = state

    def decide_next_action(self, sources, machines):
        """Decide what to do next based on the current state."""
        if self.state == State.Idle:
            if not self.inventory_full():
                # Find a source to collect from
                for source in sources.get_piece_array():
                    self.set_destination(source.get_location())
                    self.set_state(State.Collect)
                    break
            elif self.inventory_full():
                # Go to the machine to sell
                self.set_destination(machines.get_items()["$"][0].get_location())
                self.set_state(State.Sell)

        elif self.state == State.Collect:
            if self.at_destination() and not self.inventory_full():
                # Perform collection at destination
                self.set_state(State.Idle)

        elif self.state == State.Sell:
            if self.at_destination() and not self.any_in_inventory():
                # Finished selling, return to idle
                self.set_state(State.Idle)

class MinerRobot(NPC):
    def __init__(self, name: str, location: Tuple[int, int] = (0, 0)):
        super().__init__(Type.Robot, name, symbol="*", location=location, state=State.Idle)
        self.add_inventory_type("@")  # Miner-specific inventory type
    
class Player(Character):

    def __init__(self, name: str, symbol: str):
        super().__init__(Type.Player, name=name, symbol=symbol)
        self.money = 0
    
    def next_move(self, direction: Direction) -> Tuple[int, int]:
        x = self.location[0] + direction.value[0]
        y = self.location[1] + direction.value[1]
        return (x, y)

    def validate_move(self, move: Tuple[int, int]):
        diff_x = move[0] - self.location[0]
        diff_y = move[1] - self.location[1]

        # we can only move one square at a time
        return abs(diff_x) + abs(diff_y) == 1

    def move(self, move: Tuple[int, int]):
        self.location = move

    def get_money(self):
        return self.money

    def add_money(self, amount):
        if amount > 0:
            self.money += amount

    def remove_money(self, amount):
        if amount > 0:
            self.money -= amount

    # can probably make this better and merged with NPC interaction logic
    # this is so bad how NPC manager is cyclically referenced.. fix. probably outside of loop
    def calculate_interactions(self, sources: SourceManager, machines: MachineManager):
        for source in sources.get_piece_array():
            if self.get_location() == source.get_location():
                item = source.take()
                if item:
                    self.add_to_inventory(item)
                    return

        for machine in machines.get_piece_array():
            if self.get_location() == machine.get_location():
                if self.any_in_inventory():
                    item = self.get_inventory().pop()
                    self.add_money(machine.convert(item))
                    BroadCast().announce(f"You sold {item.get_symbol()} for ${item.get_worth()}")
                    return
    
    def purchase_from_shop(self, shops: ShopManager, ticks: int) -> Tuple[bool, str, str]:
        """
        Attempt to purchase from a shop. Return a tuple indicating success,
        the shop symbol, and the item type purchased.
        """
        for shop in shops.get_piece_array():
            if self.get_location() == shop.get_location():
                price = shop.get_price()

                if self.get_money() >= price:
                    if shop.purchase(ticks):
                        self.remove_money(price)
                        return True, shop.get_item_symbol(), shop.get_item()
        
        return False, "", ""
