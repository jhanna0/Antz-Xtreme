# Built in
import time
import threading
import random

# Objects
from Game.board import Board
from Pieces.player import Player
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Game.bank import Bank

# Managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Pieces.machine import MoneyMachine
from Managers.source_manager import SourceManager

# Control and View
from Game.display import Display
from Game.broadcast import BroadCast
from Game.controller import Controller
from Game.tick import TickManager


class Game:
    def __init__(self):
        # Viewports and Movement
        self.board = Board(10, 20)
        self.controller = Controller()
        self.display = Display(self.board)

        # Tick
        self.ticks = TickManager(tick_rate=0.4)

        # Managers
        self.npcs = NPCManager()
        self.sources = SourceManager(["@", "#", "%", "T"])
        self.machines = MachineManager()
        self.shops = ShopManager()

        # Player
        self.player_icon = "~"
        self.player = Player(symbol=self.player_icon)

        # Bank
        self.bank = Bank()

        # Register entities
        self.machines.register(MoneyMachine("$"))
        self.shops.register(Shop(piece_type=MinerRobot))

        # Events
        self.events = 0
        self.last_event_time = 0

        BroadCast().announce(f"You are '{self.player_icon}'.")
        BroadCast().announce(f"Mine resources. Sell resources at '$'.")
        BroadCast().announce(f"Purchase upgrades at '!'.")

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
        # display takes player but maybe we can avoid this
        self.display.update_display(self.bank, self.player.inventory)

    def player_move(self, key):
        next_move = self.player.next_move(self.controller.move_list[key])
        
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)
            self.update_board()
    
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
        
    # move to event class later
    def trigger_event(self):
        total_ticks = self.ticks.get_total_ticks()

        if total_ticks > 20 and self.events == 0: # first event happens early
            self.sources.create_random_source()
            self.events += 1
            self.last_event_time = total_ticks

        elif (total_ticks - self.last_event_time) >= random.randint(180, 300): # Trigger an event every ~240 ticks
            self.sources.create_random_source()
            self.last_event_time = total_ticks
            self.events += 1

    def run(self):
        controller_thread = threading.Thread(target=self.controller.listen, daemon=True)
        controller_thread.start()
        self.ticks.start()

        while self.controller.running:
            # Handle player input (sub-tick)
            key = self.controller.get_last_input()
            if key == self.controller.get_exit_key():
                self.controller.stop()
                break

            if key and key in self.controller.move_list and self.ticks.is_sub_tick():
                self.player_move(key)

            if self.ticks.is_full_tick():

                self.sources.update(self.ticks.get_game_time())

                self.player_turn_sequence()
                self.npcs.turn_sequence(self.sources, self.machines)

                self.trigger_event()
                self.update_board()

            time.sleep(0.01)


game = Game()
game.run()
