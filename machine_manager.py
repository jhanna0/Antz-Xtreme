from board import Board
from machine import Machine
from typing import Dict
from characters import Player

class MachineManager:
    def __init__(self, board: Board):
        self.machines: Dict[str, Machine] = {}
        self.board = board

    def register(self, symbol: str, machine: Machine):
        self.machines[symbol] = machine
        self.board.update_piece_position(self.machines)

    def calculate_player_interaction(self, player: Player):
        for machine in self.machines.values():
            if player.get_location() == machine.get_location():
                inv = player.get_inventory()
                if inv:
                    item = inv.pop()
                    player.add_money(machine.convert(item))
