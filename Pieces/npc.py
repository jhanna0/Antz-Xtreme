from typing import Tuple

from Pieces.character import Character
from Game.definitions import NpcState
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

class NPC(Character):
    def __init__(self, sources: SourceManager, machines: MachineManager, name: str, location: Tuple[int, int], symbol: str):
        super().__init__(name, location, symbol, sources, machines)
        self.destination: Tuple[int, int] = location
        self.state: NpcState = NpcState.Idle
        self.sources = sources
        self.machines = machines

    def move(self) -> None:
        """
        Moves the NPC one step closer to its destination.
        """
        x, y = self.location
        dest_x, dest_y = self.destination

        # Vertical then horizontal movement
        if x != dest_x:
            x += 1 if dest_x > x else -1
        elif y != dest_y:
            y += 1 if dest_y > y else -1

        self.location = (x, y)

    def decide_next_action(self) -> None:
        """
        Decides the NPC's next destination or action based on game state.
        """
        raise NotImplementedError()

    def at_destination(self) -> bool:
        """
        Checks if the NPC has reached its destination.
        """
        return self.location == self.destination

    def set_destination(self, destination: Tuple[int, int]) -> None:
        """
        Sets the NPC's next destination.
        """
        self.destination = destination
