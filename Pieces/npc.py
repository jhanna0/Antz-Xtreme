from typing import Tuple

from Pieces.character import Character
from Game.definitions import NpcState
from Game.bank import Bank

class NPC(Character):
    def __init__(self, name: str, symbol: str, location: Tuple[int, int], bank: Bank):
        super().__init__(name, symbol, location, bank)
        self.destination: Tuple[int, int] = (0, 0)
        self.state: NpcState = NpcState.Idle

    def move(self) -> None:
        # move NPC one step
        x, y = self.location
        dest_x, dest_y = self.destination

        dx = dest_x - x
        dy = dest_y - y

        # Vertical then horizontal
        if dx != 0:
            x += 1 if dx > 0 else -1
        elif dy != 0:
            y += 1 if dy > 0 else -1

        self.location = (x, y)
    
    def decide_next_action(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented decide_next_action")

    def get_destination(self) -> Tuple[int, int]:
        return self.destination

    def set_destination(self, destination: Tuple[int, int]) -> None:
        self.destination = destination

    def at_destination(self) -> bool:
        return self.destination == self.location

    def transition_state(self, state: NpcState) -> None:
        # can add broadcast here
        self._set_state(state)

    def _set_state(self, state: NpcState) -> None:
        self.state = state


