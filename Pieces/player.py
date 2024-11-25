from Pieces.character import Character
from Game.definitions import Direction
from typing import Tuple
from Game.broadcast import broadcast
from Game.bank import bank
from Managers.machine_manager import MachineManager
from Managers.source_manager import SourceManager
from Game.board import Board

class Player(Character):

    def __init__(self, name: str = "You", location: Tuple[int, int] = (0,0), symbol: str = "~"):
        super().__init__(name, location, symbol)
        self.last_direction = Direction.Right
    
    def next_move(self, direction: Direction) -> Tuple[int, int]:
        x = self.location[0] + direction.value[0]
        y = self.location[1] + direction.value[1]
        self.last_direction = direction
        return (x, y)

    def validate_move(self, move: Tuple[int, int]) -> bool:
        diff_x = move[0] - self.location[0]
        diff_y = move[1] - self.location[1]

        # we can only move one square at a time
        return abs(diff_x) + abs(diff_y) == 1

    def move(self, move: Tuple[int, int]) -> None:
        self.location = move

    def turn_sequence(self, sources: SourceManager, machines: MachineManager) -> None:
        # we basically have this in NPC manager already... repeated logic, but might make sense to keep this in Player for now
        # although, it might be better to have Player ignorant of whole game state and just worry about self
        """
        Handles the player's interactions and movement for this turn.
        """
        self._interact_with_source(sources)
        self._interact_with_machine(machines)

    def _interact_with_source(self, sources: SourceManager) -> None:
        """
        Handle interactions with sources at the player's location.
        """
        source = sources.get_piece_at_location(self.get_location())
        if source:
            self.interact_with_source(source)

    def _interact_with_machine(self, machines: MachineManager) -> None:
        """
        Handle interactions with machines at the player's location.
        """
        machine = machines.get_piece_at_location(self.get_location())
        if machine:
            self.interact_with_machine(machine)

    def move_player(self, board: Board, direction: Direction) -> None:
        """
        Move the player in the given direction, if the move is valid.
        """
        next_move = self.next_move(direction)
        if board.validate_move(next_move) and self.validate_move(next_move):
            self.move(next_move)
    
    def interact_with_shop(self):
        # didn't use shops for anything yet!
        pass
