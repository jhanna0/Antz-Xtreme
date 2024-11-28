from Game.board import Board
from typing import List
from Game.broadcast import broadcast
from Game.bank import bank
from Inventory.inventory import Inventory

class Display:
    def __init__(self, board: Board, inventory: Inventory):
        self.board = board
        self.inventory = inventory
        self.messages: List[str] = []
        self.last_message = None  # Tracks the last unique message
        self.last_message_count = 0  # Tracks how many times the last message was repeated
        self.story_name = ""  # Story name to display
        self.objective = ""  # Objective to display
        self.chapter_name = ""  # Chapter name to display
        self.starting_row = 1  # Tracks the row where the content starts
        broadcast.subscribe(self)
        self.clear_screen()

    def set_story_name(self, name: str):
        """Sets the story name to be displayed."""
        self.story_name = name

    def set_chapter_name(self, name: str):
        """Sets the chapter name to be displayed."""
        self.chapter_name = name

    def set_objective(self, objective: str):
        """Sets the objective to be displayed."""
        self.objective = objective

    def add_message(self, msg: str):
        """Adds a message to the message log, consolidating repeated messages."""
        if self.last_message == msg:
            # Increment the count for the last message
            self.last_message_count += 1
            # Update the last message with the new count
            self.messages[-1] = f"{msg} ({self.last_message_count})"
        else:
            # Reset the count for a new message
            self.last_message = msg
            self.last_message_count = 1
            # Add the new message
            self.messages.append(msg)
            if len(self.messages) > 3:
                self.messages.pop(0)

        self.update_messages()

    def clear_messages(self):
        """Clears the message log."""
        self.messages = []

    def clear_screen(self):
        """Clears the terminal screen."""
        print("\033[H\033[J", end="")  # Move cursor to the top-left and clear the screen

    def update_display(self):
        """Updates the display with the current game state, dynamically positioning elements."""
        self.clear_screen()
        rows, cols = self.board.get_size()
        money_string = bank.get_money_string()
        inventory_string = "[" + ' '.join(self.inventory.get_items_symbols()) + "]"

        spacing = (cols * 2) - (len(money_string) + len(inventory_string)) - 1

        current_row = self.starting_row

        # Story name and details
        current_row = self._print_section(current_row, self.story_name)
        current_row = self._print_section(current_row, self.chapter_name)
        current_row = self._print_section(current_row, self.objective)

        # Game board
        for row in self.board.get_board():
            print(f"\033[{current_row};1H", end="")
            print(' '.join([str(x) for x in row]))
            current_row += 1

        # Player info
        print(f"\033[{current_row};1H", end="")
        print(f"{money_string}{' ' * spacing}{inventory_string}")
        current_row += 2  # Space below player info

        # Messages
        self.update_messages(current_row)

    def update_messages(self, starting_row: int = None):
        """Updates the message section starting at the specified row."""
        rows, cols = self.board.get_size()
        if starting_row is None:
            starting_row = self.starting_row  # Use default starting row
        for i, message in enumerate(self.messages):
            print(f"\033[{starting_row + i};1H", end="")
            print(f"{message:<80}")  # Clear any leftover text by padding with spaces

    def _print_section(self, start_row: int, content: str) -> int:
        """Helper to print a single line of content and return the next row index."""
        if content:
            print(f"\033[{start_row};1H{content}")
            return start_row + 1
        return start_row
