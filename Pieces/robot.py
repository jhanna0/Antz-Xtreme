from typing import Set, Tuple

from Pieces.npc import NPC
from Game.definitions import NpcState
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

# pass location in future from NPCManager
class MinerRobot(NPC):
    def __init__(self,
            name: str,
            location: Tuple[int, int],
            sources: SourceManager,
            machines: MachineManager,
            symbol: str = "~"):
        
        super().__init__(
            name = name,
            location = location,
            symbol = symbol,
            sources = sources,
            machines = machines
            )
        self.inventory_types: Set[str] = set()

    # NOT USED. eventually will be used to target specific sources
    def add_inventory_type(self, item_type: str) -> None:
        self.inventory_types.add(item_type)

    # can maybe be Piece/Source instead of str
    def get_inventory_types(self) -> Set[str]:
        return self.inventory_types

    # i don't know.. let's keep sources in here for now... but could move out of here and only pass sources.get_best_source()
    # two sides to the coin: 1 NPC manager should tell NPC what to do, but also, NPC can decide what to do on its own!
    def decide_next_action(self):
        if self.state == NpcState.Idle:
            # we need to check if NPC is at destination !!
            if not self.inventory_full():
                # Find and move to the best source
                # multiple NPCs will now go after this source! -> another reason to move logic to NPC manager
                # get best source only calculates quantity, not what the npc needs. need to figure out best source here i think
                source = self.sources.get_best_source(self.get_location())
                if source:
                    self.set_destination(source.get_location())
                    self.transition_state(NpcState.Collect)

            elif self.inventory_full():
                # Move to the nearest machine to sell inventory
                machine = self.machines.get_nearest_piece(self.get_location())
                if machine:
                    self.set_destination(machine.get_location())
                    self.transition_state(NpcState.Sell)

        elif self.state == NpcState.Collect:
            if self.inventory_full():
                # could just switch to collect but switching to Idle seems safer for now
                self.transition_state(NpcState.Idle)

            elif self.at_destination():
                source = self.sources.get_piece_at_location(self.get_location())
                if source and source.is_depleted():
                    # Perform collection at destination
                    self.transition_state(NpcState.Idle)
                
                # source has expired
                elif not source:
                    self.transition_state(NpcState.Idle)

        elif self.state == NpcState.Sell:
            if self.at_destination() and not self.any_in_inventory():
                # Finished selling, return to idle
                self.transition_state(NpcState.Idle)
    
    def transition_state(self, state: NpcState):
        self.state = state
