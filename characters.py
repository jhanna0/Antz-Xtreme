from enum import Enum
from typing import Tuple, Dict
from source import Source
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

class Character():

    def __init__(self, self_type: Type, name: str, location: Tuple = (0, 0)):
        self.type = self_type
        self.name = name
        self.location = location
        self.inventory: Inventory = Inventory()

    def get_location(self):
        return self.location

    def move(self):
        raise NotImplementedError(f"Move not implemented in {self.type} {self.name}")
    
    def add_to_inventory(self, item):
        self.inventory.add_to_inventory(item)

    def get_inventory(self):
        return self.inventory.get_items()

    def get_capacity(self):
        return self.inventory.get_capacity()

    def get_type(self):
        return "Character"
    
    def inventory_full(self) -> bool:
        return self.inventory.is_inventory_full()

    def any_in_inventory(self) -> bool:
        return self.inventory.is_there_anything_in_inventory()

class NPC(Character):
    def __init__(self, type: Type, name: str, state: State = State.Idle):
        super().__init__(type, name, (9, 18))
        self.destination: Tuple = (0, 0)
        self.inventory_types = set()
        self.state = state

    def move(self) -> Tuple[int, int]:
        """Move the robot one step toward its destination."""
        x, y = self.location
        dest_x, dest_y = self.destination

        # Determine direction of movement
        dx = dest_x - x
        dy = dest_y - y

        # Move in the direction that minimizes the distance
        if dx != 0:  # Prioritize vertical movement if needed
            x += 1 if dx > 0 else -1
        elif dy != 0:  # If aligned vertically, move horizontally
            y += 1 if dy > 0 else -1

        # Update the robot's location
        self.location = (x, y)

        return self.location

    def set_destination(self, destination: Tuple):
        self.destination = destination

    def get_destination(self):
        return self.destination

    def add_inventory_type(self, item_type: str):
        self.inventory_types.add(item_type)

    def get_inventory_types(self):
        return self.inventory_types

    def at_destination(self):
        return self.destination == self.location

    def set_state(self, state: State):
        self.state = state

    def decide_next_action(self, sources: Dict[str, Source], machines: Dict[str, Machine]):
        """Decide what to do next based on the current state."""
        if self.state == State.Idle:
            # If idle, decide whether to collect or sell
            if not self.inventory_full():
                # Find a source to collect from
                for s in sources.values():
                    self.set_destination(s.get_location())
                    self.set_state(State.Collect)
                    break

            elif self.inventory_full():
                # Go to the machine to sell
                self.set_destination(machines["$"].get_location())
                self.set_state(State.Sell)

        elif self.state == State.Collect:
            # If collecting, check if at destination
            if self.at_destination():
                if self.inventory_full():
                    self.set_state(State.Idle)  # Switch to idle to decide next action

        elif self.state == State.Sell:
            # If selling, check if at destination
            if self.at_destination() and not self.any_in_inventory():
                self.set_state(State.Idle)  # Switch to idle after selling

class MinerRobot(NPC):
    def __init__(self, name: str):
        super().__init__(Type.Robot, name, State.Idle)
    
class Player(Character):

    def __init__(self, name: str):
        super().__init__(Type.Player, name)
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
    def calculate_interactions(self, sources: Dict[str, Source], machines: Dict[str, Machine]):
        for source in sources.values():
            if self.get_location() == source.get_location():
                item = source.take()
                if item:
                    self.add_to_inventory(item)
                    return

        for machine in machines.values():
            if self.get_location() == machine.get_location():
                if self.any_in_inventory():
                    item = self.get_inventory().pop()
                    self.add_money(machine.convert(item))
                    BroadCast().announce(f"You sold {item.get_symbol()} for ${item.get_worth()}")
                    return
    
    def purchase_from_shop(self, shops: Dict[str, Shop]) -> Tuple[bool, str, str]:
        """
        Attempt to purchase from a shop. Return a tuple indicating success,
        the shop symbol, and the item type purchased.
        """
        for shop in shops.values():
            if self.get_location() == shop.get_location():
                price = shop.get_price()

                if self.get_money() >= price:
                    if shop.purchase():
                        self.remove_money(price)
                        return True, shop.get_item_symbol(), shop.get_item()
        
        return False, "", ""
