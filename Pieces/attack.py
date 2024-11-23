from typing import Tuple, List, Set
from Pieces.piece import Piece
from Game.definitions import Direction
from Game.board import Board
from Managers.manager import Manager
from Managers.npc_manager import NPCManager
from Game.broadcast import broadcast
from Game.tick import ticks

class Attack(Piece):
    def __init__(self, location: Tuple[int, int], affects: List[Manager], symbol: str = "*"):
        super().__init__(location, symbol)
        self.affects = affects
    
    # could pass in "affeced type" or something but separately is fine for now
    def calculate_impact(self) -> List[Piece]:
        raise NotImplementedError()

    def validate_next_turn(self):
        raise NotImplementedError()
    
    def next_turn(self) -> None:
        raise NotImplementedError()

class Projectile(Attack):
    def __init__(self, location: Tuple[int, int], board: Board, direction: Direction, affects: List[Manager]):
        super().__init__(location = location, affects = affects)
        self.board = board
        self.direction = direction.value
        self.hits = 0

    def calculate_impact(self) -> List[Piece]:
        all_hits: Set = set()
        for manager in self.affects:
            hits = manager.get_all_pieces_at_location(self.get_location())
            for piece in hits:
                self.hits += len(hits)
                manager.remove_piece(piece)
        return all_hits

    # same method in player class -> could make a "movable" piece class. npc doesn't take this because we assume all their moves are valid
    def validate_next_turn(self) -> bool:
        return self.board.validate_move(self._next_move()) and self.hits == 0

    def next_turn(self) -> None:
        self.location = self._next_move()

    def _next_move(self) -> Tuple[int, int]:
        x = self.location[0] + self.direction[0]
        y = self.location[1] + self.direction[1]
        return (x, y)

class Ultimate(Attack):
    def __init__(self, size: Tuple[int, int], affects: List[Manager]):
        super().__init__(location = (0, 0), affects = affects)
        self.set_size(size)
        self.start_tick = ticks.get_current_tick()
        self.duration = 5
        # broadcast.announce(f"{self.get_size()}, {self.get_footprint()}, {self.get_symbol()}")

    def calculate_impact(self) -> List[Piece]:
        affected_pieces = []
        for manager in self.affects:
            all_pieces = manager.get_pieces()
            affected_pieces.extend(all_pieces)
            for piece in all_pieces:
                manager.remove_piece(piece)
        return affected_pieces

    def validate_next_turn(self) -> bool:
        return ticks.get_tick_difference(self.start_tick) < self.duration

    def next_turn(self) -> None:
        pass
