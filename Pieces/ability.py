from typing import Tuple, List, Set
from Pieces.piece import Piece
from Pieces.player import Player
from Game.board import Board
from Managers.manager import Manager
from Game.broadcast import broadcast
from Game.tick import ticks
from Game.definitions import Direction, Speed
from Managers.npc_manager import NPCManager
from Pieces.robot import MinerRobot
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

# Abilities should maybe be a new Class, "Action"... they don't *really* need to exist on board, but a Piece
# Right now Piece is our visual (gets placed on board) Object
# But having Enum Speed begs for all actions to have start_action method .. wait for Speed .. take_action method
class Ability(Piece):
    def __init__(self, location: Tuple[int, int], affects: List[Manager], symbol: str = "*"):
        super().__init__(location, symbol)
        self.affects = affects
    
    # could pass in "affeced type" or something but separately is fine for now
    def take_action(self) -> None:
        raise NotImplementedError()

    def is_attack_finished(self) -> bool:
        raise NotImplementedError()

class Projectile(Ability):
    def __init__(self, location: Tuple[int, int], board: Board, direction: Direction, affects: List[Manager]):
        super().__init__(location = location, affects = affects)
        self.board = board
        self.direction = direction.value
        self.hits = 0

    def take_action(self) -> None:
        for manager in self.affects:
            hits = manager.get_all_pieces_at_location(self.get_location())
            for piece in hits:
                self.hits += len(hits)
                manager.remove_piece(piece)
        self.location = self._next_move()

    # same method in player class -> could make a "movable" piece class. npc doesn't take this because we assume all their moves are valid
    def is_attack_finished(self) -> bool:
        return not self.board.validate_move(self._next_move()) or not self.hits == 0

    def _next_move(self) -> Tuple[int, int]:
        x = self.location[0] + self.direction[0]
        y = self.location[1] + self.direction[1]
        return (x, y)

class Ultimate(Ability):
    def __init__(self, size: Tuple[int, int], affects: List[Manager]):
        super().__init__(location = (0, 0), affects = affects)
        self.set_size(size)
        self.start_tick = ticks.get_current_tick()
        self.duration = 5
        # broadcast.announce(f"{self.get_size()}, {self.get_footprint()}, {self.get_symbol()}")

    def take_action(self) -> None:
        for manager in self.affects:
            all_pieces = manager.get_pieces()
            for piece in all_pieces:
                manager.remove_piece(piece)

    def is_attack_finished(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration
    
# we could have this work on other Characters just need to add the properties
class Teleport(Ability):
    def __init__(self, target: Player, board_size: Tuple[int, int]):
        super().__init__(location=(0, 0), affects=[], symbol="^")
        self.target = target
        self.board_size = board_size
        self.duration = Speed.NORMAL.value
        self.start_tick = ticks.get_current_tick()

        self.start_location = self.target.get_location()
        self.destination = self._calculate_destination()

        self.set_location(self.destination)

    def take_action(self) -> None:
        """Teleport the target to the destination when the duration ends."""
        if self.is_attack_finished():
            self.target.set_location(self.destination)

    def is_attack_finished(self) -> bool:
        """Check if the teleport duration has elapsed."""
        return ticks.get_tick_difference(self.start_tick) > self.duration

    def _calculate_destination(self) -> Tuple[int, int]:
        """Calculate the final destination based on direction and board size."""
        direction = self.target.last_direction
        row, col = self.start_location  # Use the locked starting location
        dr, dc = direction.value
        max_row, max_col = self.board_size

        # Calculate the farthest valid position in the given direction
        final_row = max(0, min(max_row - 1, row + dr * (max_row if dr != 0 else max_col)))
        final_col = max(0, min(max_col - 1, col + dc * (max_col if dc != 0 else max_row)))

        return final_row, final_col

class Ring(Ability):
    def __init__(self, player: Player, affects: List[Manager]):
        super().__init__(location = (0, 0), affects = affects)
        self.set_size((3, 3))
        self.start_tick = ticks.get_current_tick()
        self.duration = 20
        self.player = player

    def take_action(self) -> None:
        self._determine_location()
        for manager in self.affects:
            for radius in self._determine_hits():
                hits = manager.get_all_pieces_at_location(radius)
                for piece in hits:
                    manager.remove_piece(piece)

    def is_attack_finished(self) -> bool:
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
            npcs: NPCManager,
            sources: SourceManager,
            machines: MachineManager
            ):
        super().__init__(location = location,affects = [], symbol = ".")
        self.duration = Speed.NORMAL.value
        self.npcs = npcs
        self.sources = sources
        self.machines = machines
        self.start_tick = ticks.get_current_tick() # definitely make an Action class

    def take_action(self) -> List[Piece]:
        if self.is_attack_finished():
            self.npcs.register(
                MinerRobot(
                    name = "Spawn",
                    location = self.location,
                    sources = self.sources,
                    machines = self.machines
                )
            )

    def is_attack_finished(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) > self.duration
