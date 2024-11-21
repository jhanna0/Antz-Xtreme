from Pieces.npc import NPC
from typing import Set, Tuple

# pass location in future from NPCManager
class MinerRobot(NPC):
    def __init__(self, name: str, symbol: str = "*", location: Tuple[int, int] = (9, 18)):
        super().__init__(name, symbol, location)
        self.inventory_types: Set[str] = set()
        self.add_inventory_type("@")

    # eventually will be used to target specific sources
    def add_inventory_type(self, item_type: str) -> None:
        self.inventory_types.add(item_type)

    # can maybe be Piece/Source instead of str
    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types
