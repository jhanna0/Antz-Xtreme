# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
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

        self.story: Story = AntzStory(self.context, self.register_keybinding)

    def _update_board(self):
        self.context.update_all_objects()
        self.board.update_piece_position(self.context.get_all_objects())
        self.display.update_display()

    def _register_default_keybindings(self):
        # default movement keys that should be used for every Game
        for key, direction in self.move_list.items():
            self.register_keybinding(key, lambda direction = direction: self.player.move_player(self.board, direction))

    def register_keybinding(self, key: str, action: callable):
        self.key_bindings[key] = action

    def handle_input(self):
        key = self.controller.process_latest_input()
        action = self.key_bindings.get(key)
        if action:
            action()

    def turn_sequence(self):
        # potential to call all managers turn_sequence here, expect only need full/half tick...
        self.player.turn_sequence(self.sources, self.machines)
        self.abilities.turn_sequence()
        self.npcs.turn_sequence(self.sources, self.machines)
        self.sources.turn_sequence()
        self.handle_input()
        self._update_board()

    # should we move to a true tick system where all actions have durations?
    def run(self):
        self.controller.start()
        self.story.start()

        while self.controller.running:
            if ticks.check_game_loop_tick():
                self.turn_sequence()

            # Handle the story progression or win state
            if not self.story.win_condition():
                self.story.play()

            else:
                self.story.win() # this keeps getting called until we break

            ticks.wait_until_next_tick()
            
game = Game()
game.run()
