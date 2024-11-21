# built in
import time
import threading
import random

# objects
from Game.board import Board
from Pieces.character import Player, MinerRobot
from Pieces.shop import Shop

# managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Pieces.machine import MoneyMachine
from Managers.source_manager import SourceManager

# control and view
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
        self.tick = TickManager(tick_rate=0.4)

        # Managers
        self.npcs = NPCManager()
        self.sources = SourceManager(self.board, ["@", "#", "%", "T"])
        self.machines = MachineManager()
        self.shops = ShopManager()

        # Player
        self.player_icon = "~"
        self.player = Player(name="Player 1", symbol=self.player_icon)

        # Register entities
        self.machines.register(MoneyMachine("$"))
        self.shops.register(Shop("!", "*", "robot"))

        # Events
        self.events = 0
        self.last_event_time = 0

        BroadCast().announce(f"You are '{self.player_icon}'.")
        BroadCast().announce(f"Mine resources. Sell resources at '$'.")
        BroadCast().announce(f"Purchase upgrades at '!'.")

    def update_board(self):
        # if adding new type of pieces, add here
        all_objects = {
            self.player_icon: [self.player],
            **self.npcs.items,
            **self.sources.items,
            **self.machines.items,
            **self.shops.items,
        }

        self.board.update_piece_position(all_objects)
        # display takes player but maybe we can avoid this
        self.display.update_display(self.player)

    def player_move(self, key):
        next_move = self.player.next_move(self.controller.move_list[key])
        
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)
            self.update_board()
    
    def trigger_event(self):
        total_ticks = self.tick.get_total_ticks()

        # first event happens early
        if total_ticks > 20 and self.events == 0:
            self.sources.create_random_source()
            self.events += 1
            self.last_event_time = total_ticks
            return

        # Trigger an event every ~200 ticks
        elif (total_ticks - self.last_event_time) >= random.randint(180, 300):
            self.sources.create_random_source()
            self.last_event_time = total_ticks
            self.events += 1

    def run(self):
        controller_thread = threading.Thread(target=self.controller.listen, daemon=True)
        controller_thread.start()
        self.tick.start()

        while self.controller.running:
            # Handle player input (sub-tick)
            key = self.controller.get_last_input()
            if key == self.controller.get_exit_key():
                self.controller.stop()
                break

            if key and key in self.controller.move_list and self.tick.is_sub_tick():
                self.player_move(key)

            if self.tick.is_full_tick():

                self.sources.update(self.tick.get_game_time())
                self.npcs.move_and_set_destinations(self.sources, self.machines)

                self.player.calculate_interactions(
                    self.sources,
                    self.machines,
                )

                # ugliest bit of code in the whole program here. @K1 FIX!!!
                success, shop_symbol, item = self.player.purchase_from_shop(self.shops, self.tick.get_total_ticks())
                if success:
                    if item == "robot":
                        # Add logic to create and register a new NPC
                        robot = MinerRobot(name="QT", location=(9, 18))
                        self.npcs.register(robot)
                        BroadCast().announce(f"A {robot.get_type()}, {robot.name}, joins your team!")

                # Handle NPC interactions separately
                self.npcs.calculate_interactions(
                    self.sources,
                    self.machines,
                    self.player
                )

                self.trigger_event()
                self.update_board()

            time.sleep(0.01)


game = Game()
game.run()
