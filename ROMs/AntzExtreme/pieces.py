from typing import Set, Tuple, List, Any, TYPE_CHECKING

from Pieces.npc import NPC
from Pieces.piece import Piece
from Pieces.player import Player
from Game.definitions import NpcState, Direction, Speed, Rarity, superscript_mapping, SignalType, source_rarity_weights, source_creation_rate, source_worth_map
from Game.board import Board
from Game.tick import ticks
from Game.broadcast import broadcast
from Game.signals import signals
from Game.bank import bank
from Inventory.item import Item

if TYPE_CHECKING:
    from Game.context import GameContext

# --- SOURCES & MACHINES ---
# These were previously in core, now part of the specific game ROM

class Source(Piece):
    def __init__(self, symbol: str, location: Tuple[int, int], creation_rate: float, worth: int, rarity: Rarity):
        super().__init__(location, symbol, size=(1, 2))
        self.capacity = 6
        self.quantity = 0
        self.last_grow = 0
        self.creation_rate = creation_rate  # Time interval to create new items
        self.worth = worth  # Value of the source items
        self.rarity = rarity
        self.item = Item(symbol, worth)
        self.lifetime = 10

    def grow(self):
        game_tick = ticks.get_current_tick()
        if (game_tick - self.last_grow) > self.creation_rate and self.quantity < self.capacity:
            self.last_grow = game_tick
            self.quantity += 1

    def get_quantity(self):
        return self.quantity
    
    def is_depleted(self):
        return self.quantity == 0

    def take(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.lifetime -= 1
            return self.item
        return None

    def get_footprint(self) -> str:
        return f"{self.symbol}{superscript_mapping.get(self.quantity, self.quantity)}"
    
    def update(self) -> None:
        self.grow()

    def is_expired(self) -> bool:
        return self.lifetime <= 0

def create_random_source(generator, manager):
    # This helper was in generate.py but is game-specific
    potential_sources = (97, 123)
    symbol = chr(generator.choose_from_range(potential_sources))
    location = generator.find_location_for_piece((1, 2)) 

    rarity = generator.choose_rarity(source_rarity_weights)
    creation_rate = generator.choose_from_list(source_creation_rate[rarity])
    worth = generator.choose_from_list(source_worth_map[rarity])
    source = Source(symbol, location, creation_rate, worth, rarity)
    manager.register(source)

class Machine(Piece):
    def __init__(self, symbol: str, location: Tuple[int, int] = (4, 0)): 
        super().__init__(location, symbol)
        self.efficiency = 1

    def convert(self, item: Item):
        raise NotImplementedError(f"Convert not implemented")
    
    def get_symbol(self):
        return self.symbol

# --- PLAYERS & ROBOTS ---

# An enhanced player that knows how to interact with Sources and Machines
class AntzPlayer(Player):
    def __init__(self, name: str = "You", location: Tuple[int, int] = (0, 0), symbol: str = "~"):
        super().__init__(name, location, symbol)
        # Subscribe to interaction signals
        signals.subscribe(SignalType.INTERACT_WITH_SOURCE, self._handle_source_interaction)
        signals.subscribe(SignalType.INTERACT_WITH_MACHINE, self._handle_machine_interaction)

    def _handle_source_interaction(self, signal):
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
        if signal.data.get("target") != self:
            return
        machine = signal.data.get("machine")
        if machine and self.any_in_inventory():
            item = self.get_inventory().pop()
            bank.add_money(machine.convert(item))
            broadcast.announce(f"{self.name} sold {item.get_symbol()} for ${item.get_worth()}")

class MinerRobot(NPC):
    def __init__(self,
            context: 'GameContext',
            name: str,
            location: Tuple[int, int],
            symbol: str = "~"):
        
        super().__init__(
            context = context,
            name = name,
            location = location,
            symbol = symbol
            )
        self.inventory_types: Set[str] = set()

    def add_inventory_type(self, item_type: str) -> None:
        self.inventory_types.add(item_type)

    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types

    def decide_next_action(self):
        if self.state == NpcState.Idle:
            if not self.inventory_full():
                # Find and move to the best source
                sources = self.context.get_entities(Source)
                
                candidates = [s for s in sources if not s.is_depleted()]
                if not candidates:
                    candidates = sources
                
                if candidates:
                    source = min(candidates, key=lambda s: s.get_distance_from(self.get_location()))
                    self.set_destination(source.get_location())
                    self.transition_state(NpcState.Collect)

            elif self.inventory_full():
                machine = self.context.entity_manager.get_nearest_piece(self.get_location(), Machine)
                if machine:
                    self.set_destination(machine.get_location())
                    self.transition_state(NpcState.Sell)

        elif self.state == NpcState.Collect:
            if self.inventory_full():
                self.transition_state(NpcState.Idle)

            elif self.at_destination():
                pieces = self.context.entity_manager.get_all_pieces_at_location(self.get_location())
                source = next((p for p in pieces if isinstance(p, Source)), None)
                
                if source and source.is_depleted():
                    self.transition_state(NpcState.Idle)
                
                elif not source:
                    self.transition_state(NpcState.Idle)

        elif self.state == NpcState.Sell:
            if self.at_destination() and not self.any_in_inventory():
                self.transition_state(NpcState.Idle)
    
    def transition_state(self, state: NpcState):
        self.state = state

# --- MACHINES ---

class MoneyMachine(Machine):
    def __init__(self, symbol: str, location: Tuple[int, int]):
        super().__init__(symbol, location)

    def convert(self, item: Item):
        return item.get_worth()

# --- ABILITIES ---

from Pieces.ability import Ability

class Projectile(Ability):
    def __init__(self, location: Tuple[int, int], context: 'GameContext', direction: Direction):
        super().__init__(location = location, context = context)
        self.direction = direction.value
        self.hits = 0

    def take_action(self) -> None:
        hits = self.context.entity_manager.get_all_pieces_at_location(self.get_location())
        for piece in hits:
            if piece == self: continue 
            self.hits += 1 
            self.context.entity_manager.remove_piece(piece)
        self.location = self._next_move()

    def is_complete(self) -> bool:
        return not self.context.board.validate_move(self._next_move()) or not self.hits == 0

    def _next_move(self) -> Tuple[int, int]:
        x = self.location[0] + self.direction[0]
        y = self.location[1] + self.direction[1]
        return (x, y)

class Ultimate(Ability):
    def __init__(self, size: Tuple[int, int], context: 'GameContext'):
        super().__init__(location = (0, 0), context = context)
        self.set_size(size)
        self.start_tick = ticks.get_current_tick()
        self.duration = 5

    def take_action(self) -> None:
        all_pieces = self.context.entity_manager.get_pieces()
        for piece in all_pieces:
            if piece == self: continue
            self.context.entity_manager.remove_piece(piece)

    def is_complete(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration
    
class Teleport(Ability):
    def __init__(self, target: Player, context: 'GameContext'):
        super().__init__(location=(0, 0), context=context, symbol="^")
        self.target = target
        self.duration = Speed.NORMAL.value
        self.start_tick = ticks.get_current_tick()

        self.start_location = self.target.get_location()
        self.destination = self._calculate_destination()

        self.set_location(self.destination)

    def take_action(self) -> None:
        if self.is_complete():
            self.target.set_location(self.destination)

    def is_complete(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration

    def _calculate_destination(self) -> Tuple[int, int]:
        direction = self.target.last_direction
        row, col = self.start_location 
        dr, dc = direction.value
        max_row, max_col = self.context.board.get_size()

        final_row = max(0, min(max_row - 1, row + dr * (max_row if dr != 0 else max_col)))
        final_col = max(0, min(max_col - 1, col + dc * (max_col if dc != 0 else max_row)))

        return final_row, final_col

class Ring(Ability):
    def __init__(self, player: Player, context: 'GameContext'):
        super().__init__(location = (0, 0), context = context)
        self.set_size((3, 3))
        self.start_tick = ticks.get_current_tick()
        self.duration = 20
        self.player = player

    def take_action(self) -> None:
        self._determine_location()
        for radius in self._determine_hits():
            hits = self.context.entity_manager.get_all_pieces_at_location(radius)
            for piece in hits:
                if piece == self or piece == self.player: continue
                self.context.entity_manager.remove_piece(piece)

    def is_complete(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration

    def _determine_location(self) -> None:
        row, col = self.player.get_location()
        self.set_location((row - 1, col - 1))
    
    def _determine_hits(self):
        locations = []
        height, width = self.get_size()
        row, col = self.get_location()
        for dh in range(height):
            for dw in range(width):
                locations.append((row + dh, col + dw))
        return locations

class Conjure(Ability):
    def __init__(self,
            location: Tuple[int, int],
            context: 'GameContext'
            ):
        super().__init__(location = location, context = context, symbol = ".")
        self.duration = Speed.NORMAL.value
        self.start_tick = ticks.get_current_tick() 

    def take_action(self) -> None:
        if self.is_complete():
            self.context.register_entity(
                MinerRobot(
                    context = self.context,
                    name = "Spawn",
                    location = self.location
                )
            )

    def is_complete(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration
