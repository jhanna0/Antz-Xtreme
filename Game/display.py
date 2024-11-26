from Game.board import Board
from typing import List
from Game.broadcast import broadcast
from Game.bank import bank
from Inventory.inventory import Inventory

class Display:
    def __init__(self, board: Board, inventory: Inventory):
        self.board = board
        self.messages: List[str] = []
        self.last_message = None  # Tracks the last unique message
        self.last_message_count = 0  # Tracks how many times the last message was repeated
        self.story_name = ""  # Story name to display
        self.objective = ""  # Objective to display
        self.chapter_name = ""
        broadcast.subscribe(self)
        self.clear_screen()
        self.inventory = inventory

    def set_story_name(self, name: str):
        """
        Sets the story name to be displayed.
        """
        self.story_name = name

    def set_chapter_name(self, name: str):
        """
        Sets the story name to be displayed.
        """
        self.chapter_name = name

    def set_objective(self, objective: str):
        """
        Sets the objective to be displayed.
        """
        self.objective = objective

    def add_message(self, msg: str):
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
        self.messages = []

    def clear_screen(self):
        print("\033[H\033[J", end="")  # Move cursor to the top-left and clear the screen

    def update_display(self):
        # Clear the screen and display the entire interface
        self.clear_screen()
        rows, cols = self.board.get_size()
        money_string = bank.get_money_string()
        inventory_string = "[" + ' '.join(self.inventory.get_items_symbols()) + "]"

        spacing = (cols * 2) - (len(money_string) + len(inventory_string)) - 1

        # Story name and objective
        print(f"\033[1;1H{self.story_name:<{cols * 2}}")
        print(f"\033[2;1H{self.chapter_name:<{cols * 2}}")
        print(f"\033[3;1H{self.objective:<{cols * 2}}")

        # Game board
        for i, row in enumerate(self.board.get_board()):
            print(f"\033[{i + 5};1H", end="")  # Move to the specific row (offset by 2)
            print(' '.join([str(x) for x in row]))

        # Player info
        print(f"\033[{rows + 4};1H", end="")  # Move to the row below the board
        print(f"{money_string}{' ' * spacing}{inventory_string}")

        self.update_messages()

    def update_messages(self):
        rows, cols = self.board.get_size()
        for i, message in enumerate(self.messages):
            print(f"\033[{rows + 6 + i};1H", end="")  # Reserve rows for messages
            print(f"{message:<80}")  # Clear any leftover text by padding with spaces
