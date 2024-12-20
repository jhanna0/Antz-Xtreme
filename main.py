from typing import List

# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Game.story import Story, AntzStory
from Game.context import GameContext

# Managers
from Managers.manager import Manager
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
from Game.definitions import Direction

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
        self.sources = SourceManager()
        self.machines = MachineManager()
        self.shops = ShopManager()
        self.abilities = AbilityManager(self.board)
        self.generator = Generator(self.board, self.sources) # could pass full context if needed
        self.events = Events(self.generator)

        # Player
        self.player = Player(
            symbol = "~",
            location = self.generator.find_location_for_piece(),
            sources = self.sources,
            machines = self.machines
        )

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

        # we can probably put Player actions in a Manager class to be more consistent
        self.turn_entities: List[Manager | Player] = [
            self.player,
            self.abilities,
            self.npcs,
            self.sources
        ]

        self.story: Story = AntzStory(self.context, self.register_keybinding)
        self.display.set_story_name(self.story.get_story_name())

    def register_keybinding(self, key: str, action: callable):
        self.key_bindings[key] = action

    def _update_board(self):
        self.board.update_piece_position(self.context.get_all_objects())
        self.display.set_chapter_name(self.story.get_chapter_name())
        self.display.set_objective(self.story.get_objective_name())
        self.display.update_display()

    def _register_default_keybindings(self):
        # default movement keys that should be used for every Game
        for key, direction in self.move_list.items():
            self.register_keybinding(key, lambda direction = direction: self.player.move_player(self.board, direction))

    def _handle_input(self):
        key = self.controller.process_latest_input()
        action = self.key_bindings.get(key)
        if action:
            action()

    def _turn_sequence(self):
        for entity in self.turn_entities:
            entity.turn_sequence()

        self._handle_input()
        self._update_board()

    # should we move to a true tick system where all actions have durations?
    def run(self):
        self.controller.start()
        self.story.start()

        while self.controller.running:
            if ticks.check_game_loop_tick():
                self._turn_sequence()

            # Let the story handle all its logic in a single call
            self.story.play()

            ticks.wait_until_next_tick()

game = Game()
game.run()
