from Pieces.npc import NPC
from Managers.manager import Manager
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

class NPCManager(Manager[NPC]):
    def __init__(self):
        super().__init__()
    
    def turn_sequence(self, sources: SourceManager, machines: MachineManager):
        self._handle_source_interactions(sources)
        self._handle_machine_interactions(sources)
        self._move_and_set_destinations(sources, machines)

    def _handle_source_interactions(self, sources: SourceManager):
        for npc in self.get_pieces_list():
            source = sources.get_piece_at_location(npc.get_location())
            if source:
                npc.interact_with_source(source)

    def _handle_machine_interactions(self, machines: MachineManager):
        for npc in self.get_pieces_list():
            machine = machines.get_piece_at_location(npc.get_location())
            if machine:
                npc.interact_with_machine(machine)

    def _move_and_set_destinations(self, sources: SourceManager, machines: MachineManager):
        for npc in self.get_pieces_list():
            npc.decide_next_action(sources, machines)  # Delegate fully to the NPC.. for now
            npc.move()
