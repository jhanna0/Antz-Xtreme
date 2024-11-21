from character import Character
from Game.definitions import NpcState
from Managers.source_manager import SourceManager
from Managers.machine_manager import SourceManager
from typing import Tuple, Set


class NPC(Character):
    def __init__(self, name: str, symbol: str = "*", location: Tuple[int, int] = (9, 18)):
        super().__init__(name, symbol, location)
        self.destination: Tuple[int, int] = (0, 0)
        self.state: NpcState = NpcState.Idle
        self.inventory_types: Set[str] = set()

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

    def get_destination(self) -> Tuple[int, int]:
        return self.destination

    def set_destination(self, destination: Tuple[int, int]) -> None:
        self.destination = destination

    # eventually will be used to target specific sources
    def add_inventory_type(self, item_type: str) -> None:
        self.inventory_types.add(item_type)

    # can maybe be Piece/Source instead of str
    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types

    def at_destination(self) -> bool:
        return self.destination == self.location

    def _set_state(self, state: NpcState) -> None:
        self.state = state
