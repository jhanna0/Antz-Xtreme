# Built in
import time
import threading
import random

# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.robot import MinerRobot
from Pieces.shop import Shop

# Managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Pieces.machine import MoneyMachine
from Managers.source_manager import SourceManager

# Control and View
from Game.display import Display
from Game.broadcast import broadcast
from Game.controller import Controller
from Game.tick import ticks
from Game.tutorial import Tutorial


class Game:
    def __init__(self):
        # Viewports and Movement
        self.board = Board(10, 20)
        self.controller = Controller()
        self.display = Display(self.board)

        # Managers
        self.npcs = NPCManager()
        self.sources = SourceManager(["@", "#", "%", "T"])
        self.machines = MachineManager()
        self.shops = ShopManager()
        self.events = Events(self.sources)

        # Player
        self.player_icon = "~"
        self.player = Player(symbol = self.player_icon)

        # Register entities
        self.machines.register(MoneyMachine("$"))
        self.shops.register(Shop(piece_type = MinerRobot))

        Tutorial(self.player_icon).start()

    def update_board(self):
        # if adding new type of pieces, add here
        # can make a registration method too
        all_objects = {
            self.player_icon: [self.player],
            **self.npcs.get_pieces(),
            **self.sources.get_pieces(),
            **self.machines.get_pieces(),
            **self.shops.get_pieces(),
        }

        self.board.update_piece_position(all_objects)
        # display takes player's inventory. can we avoid?
        self.display.update_display(self.player.inventory)

    def player_move(self, key):
        next_move = self.player.next_move(self.controller.move_list[key])
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)
    
    # probably can make a player manager class but do we reallllly need to just to pass every object ever??
    def player_turn_sequence(self):
        source = self.sources.get_piece_at_location(self.player.get_location())
        if source:
            self.player.interact_with_source(source)

        machine = self.machines.get_piece_at_location(self.player.get_location())
        if machine:
            self.player.interact_with_machine(machine)

        shop = self.shops.get_piece_at_location(self.player.get_location())
        if shop:
            purchase = self.player.purchase_from_shop(shop)
            if purchase:
                self.npcs.register(purchase)
                self.player_move("a") #janky but let's kick player out of shop after purchase
    
    def handle_controls(self) -> bool:
        # Handle player input (sub-tick)
        key = self.controller.get_last_input()
        if key == self.controller.get_exit_key():
            self.controller.stop()
            return False

        if key and key in self.controller.move_list and ticks.is_sub_tick():
            self.player_move(key)
        
        return True

    def run(self):
        # I think player movement runs outside of tick system
        controller_thread = threading.Thread(target = self.controller.listen, daemon = True)
        controller_thread.start()
        ticks.start()

        while self.controller.running:
            if not self.handle_controls():
                break

            if ticks.is_full_tick():
                self.sources.update(ticks.get_game_time())

                self.player_turn_sequence()
                self.npcs.turn_sequence(self.sources, self.machines)

                self.events.trigger_event(self.board.get_size())

            self.update_board()
            time.sleep(0.01)


game = Game()
game.run()
