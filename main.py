import argparse
import sys
from typing import List

# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Game.story import Story
from Stories.antz import AntzStory
from Game.context import GameContext
from Game.loader import load_story_from_file

# Managers
# from Managers.manager import Manager

# Control and View
from Game.display import Display
from Game.broadcast import broadcast
from Game.controller import Controller
from Game.tick import ticks
from Game.definitions import Direction

class Game:
    def __init__(self, story_cls):
        # Initialize viewports and movement
        self.controller = Controller()
        
        # Core components
        self.board = Board(10, 20)
        
        # Game context (starts empty, populated by Story)
        self.context = GameContext(
            board = self.board
        )

        # Movement and abilities
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.directional_ability_list = {"i": Direction.Up, "j": Direction.Left, "k": Direction.Down, "l": Direction.Right}
        self.key_bindings = {}

        # Initialize Story
        try:
            self.story: Story = story_cls(self.context, self.register_keybinding)
        except Exception as e:
             print(f"Error initializing story: {e}")
             # Print full traceback for debugging
             import traceback
             traceback.print_exc()
             sys.exit(1)
        
        # Setup Game via Story (Registers managers, creates player, etc.)
        self.story.setup(self)
        
        # Verify Player setup
        if not self.context.player:
            print("Error: Story setup failed to initialize player.")
            sys.exit(1)
            
        self.player = self.context.player

        # Display
        self.display = Display(self.board, self.player.inventory)
        self.display.set_story_name(self.story.get_story_name())

        # Key bindings
        self._register_default_keybindings()

    def register_manager(self, name: str, manager):
        # Deprecated: Managers are now unified in EntityManager
        pass

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
        # Iterate over registered managers and player
        # Note: Order of execution might matter. 
        # Currently utilizing the order in context.managers values which is insertion order (Python 3.7+)
        
        # Update Entity Manager which handles all entities
        self.context.entity_manager.update()
        
        # Player update (if separate, but could be in entity manager too)
        if hasattr(self.player, 'turn_sequence'):
             self.player.turn_sequence()

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a game story.")
    parser.add_argument("--story", type=str, help="Path to a python file containing a Story subclass")
    args = parser.parse_args()

    story_class = AntzStory
    if args.story:
        loaded_class = load_story_from_file(args.story)
        if loaded_class:
            story_class = loaded_class
        else:
            print("Failed to load custom story. Using default.")

    game = Game(story_class)
    game.run()
