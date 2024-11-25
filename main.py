from typing import List

# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Pieces.machine import MoneyMachine
from Game.story import Story, AntzStory
from Game.context import GameContext

# Managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Managers.source_manager import SourceManager
from Managers.ability_manager import AbilityManager
from Game.generate import Generator

# Control and View
from Game.display import Display
from Game.broadcast import broadcast
from Game.controller import Controller
from Game.tick import ticks
from Game.tutorial import Tutorial
from Game.definitions import Direction
from Pieces.ability import Projectile, Ultimate, Teleport, Ring, Conjure

class Game:
    def __init__(self):
        # Initialize viewports and movement
        self.controller = Controller()

        # Movement and abilities
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.directional_ability_list = {"i": Direction.Up, "j": Direction.Left, "k": Direction.Down, "l": Direction.Right}
        self.key_bindings = {}

        # Core managers
        self.board = Board(10, 20)
        self.npcs = NPCManager()
        self.generator = Generator(self.board)
        self.sources = SourceManager(self.generator)
        self.machines = MachineManager()
        self.shops = ShopManager()
        self.abilities = AbilityManager(self.board)
        self.events = Events(self.sources)

        # Player
        self.player = Player(symbol="~", location=self.generator.find_location_for_piece())

        # Display
        self.display = Display(self.board, self.player.inventory)

        # Key bindings
        self._register_default_keybindings()

        # Game context
        self.context = GameContext(
            player = self.player,
            board = self.board,
            abilities = self.abilities,
            sources = self.sources,
            npcs = self.npcs,
            machines = self.machines,
            shops = self.shops,
            generator = self.generator,
            events = self.events
        )

        self.story = AntzStory(self.context, self._register_keybinding)

    def _update_board(self):
        self.context.update_all_objects()
        self.board.update_piece_position(self.context.get_all_objects())
        self.display.update_display()

    def _register_default_keybindings(self):
        # default movement keys that should be used for every Game
        for key, direction in self.move_list.items():
            self._register_keybinding(key, lambda direction = direction: self._move_player(direction))

    def _move_player(self, direction: Direction):
        next_move = self.player.next_move(direction)
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)

    def _register_keybinding(self, key: str, action: callable):
        self.key_bindings[key] = action

    def handle_input(self):
        key = self.controller.process_latest_input()
        action = self.key_bindings.get(key)
        if action:
            action()

    def _sub_tick_sequence(self):
        self.handle_input()
        self.abilities.turn_sequence()
        self._update_board()

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

    def _full_tick_sequence(self):
        self.sources.turn_sequence()
        self.player_turn_sequence()
        self.npcs.turn_sequence(self.sources, self.machines)
        self.events.turn_sequence()
        self._update_board()

    # should we move to a true tick system where all actions have durations?
    def run(self):
        self.controller.start()
        self.story.start()

        while self.controller.running:
            sub_tick, tick = ticks.tick()
            if sub_tick:
                self._sub_tick_sequence()

            if tick:
                self._full_tick_sequence()

            # Handle the story progression or win state
            if not self.story.win_condition():
                self.story.play()

            else:
                self.story.win() # this keeps getting called until we break

            ticks.wait_until_next_tick()
            
game = Game()
game.run()
