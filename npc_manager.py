from board import Board
from characters import NPC, Player
from source import Source
from machine import Machine
from typing import Dict
from manager import Manager
from source_manager import SourceManager
from machine_manager import MachineManager
from broadcast import BroadCast

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
