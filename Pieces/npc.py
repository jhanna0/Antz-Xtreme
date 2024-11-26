from typing import Tuple

from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager
from Pieces.character import Character
from Game.definitions import NpcState

class NPC(Character):
    def __init__(self, name: str, location: Tuple[int, int], symbol: str):
        super().__init__(name, location, symbol)
        self.destination: Tuple[int, int] = location
        self.state: NpcState = NpcState.Idle

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

    def decide_next_action(self, sources: SourceManager, machines: MachineManager) -> None:
        """
        Decides the NPC's next destination or action based on game state.
        """
        # Placeholder decision logic
        self.destination = (self.location[0] + 1, self.location[1])  # Example: Move to the right

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
