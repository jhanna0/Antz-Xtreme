
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
        self.sources = SourceManager()
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

    def _update_board(self):
        # if adding new type of pieces, add here
        # can make a registration method too
        self.all_objects = {
            self.player_icon: [self.player],
            **self.npcs.get_pieces(),
            **self.sources.get_pieces(),
            **self.machines.get_pieces(),
            **self.shops.get_pieces(),
        }

        self.board.update_piece_position(self.all_objects)
        self.display.update_display(self.player.inventory) # can we avoid passing player's inventory?

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
    
    def _sub_tick_sequence(self):
        key = self.controller.process_latest_input()
        if key:
            self.player_move(key)
        self._update_board()

    def _full_tick_sequence(self):
        self.sources.update()
        self.player_turn_sequence()
        self.npcs.turn_sequence(self.sources, self.machines)
        self.events.trigger_event(self.board.get_size())
        self._update_board()

    def run(self):
        self.controller.start()

        # this is kind of turn based kind of tick based- probably can be improved
        # seems like it's kind of just sleeping between actions, but really we should be having actions take a certain amount of ticks?
        # I do like this because it blocks action
        while self.controller.running:
            sub_tick, tick = ticks.tick()
            if sub_tick:
                self._sub_tick_sequence()

            if tick:
                self._full_tick_sequence()

            ticks.wait_until_next_tick()


game = Game()
game.run()
