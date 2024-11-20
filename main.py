# built in
import time
import threading

# objects
from board import Board
from characters import Player, MinerRobot
from shop import Shop

# managers
from machine_manager import MachineManager
from npc_manager import NPCManager
from shop_manager import ShopManager
from machine import MoneyMachine
from source_manager import SourceManager

# control and view
from display import Display
from broadcast import BroadCast
from controller import Controller
from tick import TickManager


class Game:
    def __init__(self):

        # Viewports and Movement
        self.board = Board(10, 20)
        self.controller = Controller()
        self.display = Display(self.board)

        # Tick
        self.tick_rate = 0.4
        self.tick = TickManager(self.tick_rate)

        # Managers
        self.npcs = NPCManager(self.board)
        self.sources = SourceManager(self.board, ["@", "#", "%"])
        self.machines = MachineManager(self.board)
        self.shops = ShopManager(self.board)

        # Player
        self.player_icon = "~"
        self.player = Player(name="Player 1")

        # Register entities
        self.machines.register("$", MoneyMachine("$"))
        self.shops.register("!", Shop("!", "*", "robot"))

        # Events
        self.events = 0

        BroadCast().announce(f"You are '{self.player_icon}'.")
        BroadCast().announce(f"Mine resources. Sell resources at '$'.")
        BroadCast().announce(f"Purchase upgrades at '!'.")

    def update_board(self):
        all_objects = {
            self.player_icon: self.player,
            **self.npcs.npcs,
            **self.sources.sources,
            **self.machines.machines,
            **self.shops.shops,
        }
        self.board.update_piece_position(all_objects)
        self._update_display()
    
    def _update_display(self):
        self.display.update_display(self.player)

    def player_move(self, key):
        next_move = self.player.next_move(self.controller.move_list[key])
        
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)
            self.update_board()
    
    def trigger_event(self):
        # Ensure at least one event happens within the first 100 ticks
        if self.tick.get_total_ticks() > 20 and self.events == 0:
            self.sources.register_random_source()
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
                self.npcs.move_and_set_destinations(self.sources.sources, self.machines.machines)

                self.player.calculate_interactions(
                    self.sources.sources,
                    self.machines.machines,
                )

                # ugliest bit of code in the whole program here. @K1 FIX!!!
                success, shop_symbol, item = self.player.purchase_from_shop(self.shops.shops)
                if success:
                    if item == "robot":
                        # Add logic to create and register a new NPC
                        robot = MinerRobot("QT")
                        robot.add_inventory_type("@")
                        self.npcs.register(shop_symbol, robot)

                        BroadCast().announce(f"A {robot.type.value}, {robot.name}, joins your team!")

                # Handle NPC interactions separately
                self.npcs.calculate_interactions(
                    self.sources.sources,
                    self.machines.machines,
                    self.player
                )

                self.trigger_event()
                self.update_board()

            time.sleep(0.01)


game = Game()
game.run()
