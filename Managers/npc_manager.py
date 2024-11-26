from Pieces.npc import NPC
from Managers.manager import Manager
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

class NPCManager(Manager[NPC]):
    """
        Simple manager to organize NPCs
    """
    def __init__(self):
        super().__init__()

    def turn_sequence(self, sources: SourceManager, machines: MachineManager) -> None:
        """
        Executes the turn sequence for all NPCs, including interactions and movement.
        """
        for npc in self.get_pieces():
            npc.turn_sequence(sources, machines)  # Interactions handled by Character
            if not npc.at_destination():
                npc.move()
