# built in
import time
import threading
from typing import Dict

# objects
from board import Board
from characters import Player
from source import Source
from shop import Shop

# managers
from machine_manager import MachineManager
from npc_manager import NPCManager
from shop_manager import ShopManager
from machine import MoneyMachine
from source_manager import SourceManager

# control and view
from display import Display
from controller import Controller
from tick import TickManager


class Game:
    def __init__(self):
        self.board = Board(10, 20)
        self.controller = Controller()
        self.display = Display()

        # tick
        self.tick_rate = 0.6
        self.tick = TickManager(self.tick_rate)
        self.game_time = time.time()

        # Managers
        self.npcs = NPCManager(self.board)
        self.sources = SourceManager(self.board)
        self.machines = MachineManager(self.board)
        self.shops = ShopManager(self.board)

        # Player
        self.player_icon = "~"
        self.player = Player(name="Player 1")

        # Register entities
        self.sources.register("@", Source("@"))
        self.machines.register("$", MoneyMachine("$"))
        self.shops.register("!", Shop("!"))

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
        self.display.update_display(self.board.get_board(), self.player.get_money(), self.player.get_inventory())

    def player_move(self, key):
        """Handle player movement."""
        new_move = self.player.move(self.controller.move_list[key])
        if self.board.check_validate_move(self.player.get_location(), new_move):
            self.player.set_location(new_move)
            self.update_board()

    def run(self):
        """Run the game."""
        controller_thread = threading.Thread(target=self.controller.listen, daemon=True)
        controller_thread.start()
        self.tick.start()

        while self.controller.running:
            # Handle player input (sub-tick)
            key = self.controller.get_last_input()
            if key == self.controller.get_exit_key():
                print("Quit the game.")
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
                    self.shops.shops,
                    self.npcs
                )
                # Handle NPC interactions separately
                self.npcs.calculate_interactions(
                    self.sources.sources,
                    self.machines.machines,
                    self.player
                )
                self.update_board()

            time.sleep(0.01)


game = Game()
game.run()
