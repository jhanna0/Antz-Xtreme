from Pieces.character import NPC, Player
from Managers.manager import Manager
from Managers.source_manager import SourceManager
from Managers.machine_manager import MachineManager

class NPCManager(Manager):
    def __init__(self):
        super().__init__()

    # this can probably be a loop outside
    def calculate_interactions(self, sources: SourceManager, machines: MachineManager, player: Player):
        for npc in self.get_piece_array():
            # Interaction with sources
            for source in sources.get_piece_array():
                if not npc.inventory_full() and npc.get_location() == source.get_location():
                    item = source.take()
                    if item:
                        npc.add_to_inventory(item)
                        break

            # Interaction with machines
            for machine in machines.get_piece_array():
                if npc.get_location() == machine.get_location():
                    inv = npc.get_inventory()
                    if inv:
                        item = inv.pop()
                        player.add_money(machine.convert(item))

    def move_and_set_destinations(self, sources: SourceManager, machines: MachineManager):
        for npc in self.get_piece_array():
            # BroadCast().announce(str(npc))
            npc.decide_next_action(sources, machines)
            npc.move()

    def decide_next_action(self, sources: SourceManager, machines):
        """Decide what to do next based on the current state."""
        if self.state == State.Idle:
            if not self.inventory_full():
                # Find a source to collect from
                for source in sources.get_piece_array():
                    self.set_destination(source.get_location())
                    self.set_state(State.Collect)
                    break
            elif self.inventory_full():
                # Go to the machine to sell
                self.set_destination(machines.get_items()["$"][0].get_location())
                self.set_state(State.Sell)

        elif self.state == State.Collect:
            if self.at_destination() and not self.inventory_full():
                # Perform collection at destination
                self.set_state(State.Idle)

        elif self.state == State.Sell:
            if self.at_destination() and not self.any_in_inventory():
                # Finished selling, return to idle
                self.set_state(State.Idle)