from board import Board
from characters import NPC, Player
from source import Source
from machine import Machine
from typing import Dict

class NPCManager:
    def __init__(self, board: Board):
        self.npcs: Dict[str, NPC] = {}
        self.board = board

    def register(self, symbol: str, npc: NPC):
        self.npcs[symbol] = npc
        self.board.update_piece_position(self.npcs)

    # this can probably be a loop outside
    def calculate_interactions(self, sources: Dict[str, Source], machines: Dict[str, Machine], player: Player):
        for npc in self.npcs.values():
            # Interaction with sources
            for source in sources.values():
                if not npc.inventory_full() and npc.get_location() == source.get_location():
                    item = source.take()
                    if item:
                        npc.add_to_inventory(item)
                        break

            # Interaction with machines
            for machine in machines.values():
                if npc.get_location() == machine.get_location():
                    inv = npc.get_inventory()
                    if inv:
                        item = inv.pop()
                        player.add_money(machine.convert(item))

    def move_and_set_destinations(self, sources, machines):
        for npc in self.npcs.values():
            npc.decide_next_action(sources, machines)
            npc.move()
