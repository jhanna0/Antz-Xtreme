from typing import Set, Tuple

from Pieces.npc import NPC
from Game.definitions import NpcState
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager
from Game.bank import Bank

# pass location in future from NPCManager
class MinerRobot(NPC):
    def __init__(self, name: str, bank: Bank, symbol: str = "*", location: Tuple[int, int] = (9, 18)):
        super().__init__(name, symbol, location, bank)
        self.inventory_types: Set[str] = set()
        self.add_inventory_type("@")

    # eventually will be used to target specific sources
    def add_inventory_type(self, item_type: str) -> None:
        self.inventory_types.add(item_type)

    # can maybe be Piece/Source instead of str
    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types

    # i don't know.. let's keep sources in here for now... but could move out of here and only pass sources.get_best_source()
    # two sides to the coin: 1 NPC manager should tell NPC what to do, but also, NPC can decide what to do on its own!
    def decide_next_action(self, sources: SourceManager, machines: MachineManager):
        if self.state == NpcState.Idle:
            if not self.inventory_full():
                # Find and move to the best source
                # multiple NPCs will now go after this source! -> another reason to move logic to NPC manager
                source = sources.get_best_source()
                if source:
                    self.set_destination(source.get_location())
                    self.transition_state(NpcState.Collect)

            elif self.inventory_full():
                # Move to the nearest machine to sell inventory
                machine = machines.get_nearest_piece()
                if machine:
                    # why isn't this type checking get_location?
                    self.set_destination(machine.get_location())
                    self.transition_state(NpcState.Sell)

        elif self.state == NpcState.Collect:
            if self.at_destination() and not self.inventory_full():
                # Perform collection at destination
                self.transition_state(NpcState.Idle)

        elif self.state == NpcState.Sell:
            if self.at_destination() and not self.any_in_inventory():
                # Finished selling, return to idle
                self.transition_state(NpcState.Idle)
