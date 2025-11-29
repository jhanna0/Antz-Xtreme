from typing import Set, Tuple, TYPE_CHECKING

from Pieces.npc import NPC
from Pieces.source import Source
from Pieces.machine import Machine
from Game.definitions import NpcState

if TYPE_CHECKING:
    from Game.context import GameContext

# pass location in future from NPCManager
class MinerRobot(NPC):
    def __init__(self,
            context: 'GameContext',
            name: str,
            location: Tuple[int, int],
            symbol: str = "~"):
        
        super().__init__(
            context = context,
            name = name,
            location = location,
            symbol = symbol
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
                sources = self.context.get_entities(Source)
                
                # Prioritize non-depleted sources
                candidates = [s for s in sources if not s.is_depleted()]
                if not candidates:
                    candidates = sources
                
                if candidates:
                    # Find closest
                    source = min(candidates, key=lambda s: s.get_distance_from(self.get_location()))
                    self.set_destination(source.get_location())
                    self.transition_state(NpcState.Collect)

            elif self.inventory_full():
                # Move to the nearest machine to sell inventory
                machine = self.context.entity_manager.get_nearest_piece(self.get_location(), Machine)
                if machine:
                    self.set_destination(machine.get_location())
                    self.transition_state(NpcState.Sell)

        elif self.state == NpcState.Collect:
            if self.inventory_full():
                # could just switch to collect but switching to Idle seems safer for now
                self.transition_state(NpcState.Idle)

            elif self.at_destination():
                # Find Source at current location
                pieces = self.context.entity_manager.get_all_pieces_at_location(self.get_location())
                source = next((p for p in pieces if isinstance(p, Source)), None)
                
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
