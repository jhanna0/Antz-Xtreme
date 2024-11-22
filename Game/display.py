from Game.board import Board
from typing import List
from Game.broadcast import broadcast
from Game.bank import bank

class Display:
    def __init__(self, board: Board):
        self.board = board
        self.messages: List[str] = []
        self.last_message = None  # Tracks the last unique message
        self.last_message_count = 0  # Tracks how many times the last message was repeated
        broadcast.subscribe(self)
        self.clear_screen()

    def add_message(self, msg: str):
        if self.last_message == msg:
            # Increment the count for the last message
            self.last_message_count += 1
            # Update the last message with the new count
            self.messages[-1] = f"{msg} x{self.last_message_count}"
        else:
            # Reset the count for a new message
            self.last_message = msg
            self.last_message_count = 1
            # Add the new message
            self.messages.append(msg)
            if len(self.messages) > 3:
                self.messages.pop(0)

        self.update_messages()

    def clear_screen(self):
        print("\033[H\033[J", end="")  # Move cursor to the top-left and clear the screen

    def update_display(self, inventory: List[str]):
        # Entire display including board, player info, and messages
        self.clear_screen()
        rows, cols = self.board.get_size()
        money_string = bank.get_money_string()
        inventory_string = "[" + ' '.join(inventory) + "]"

        spacing = (cols * 2) - (len(money_string) + len(inventory_string)) - 1

        # game board
        for i, row in enumerate(self.board.get_board()):
            print(f"\033[{i + 1};1H", end="")  # Move to the specific row
            print(' '.join([str(x) for x in row]))
        
        # player info
        print(f"\033[{rows + 1};1H", end="")  # Move to the row below the board
        print(f"{money_string}{' ' * spacing}{inventory_string}")
        
        self.update_messages()

    def update_messages(self):
        rows, cols = self.board.get_size()
        for i, message in enumerate(self.messages):
            print(f"\033[{rows + 3 + i};1H", end="")  # Reserve rows for messages
            print(f"{message:<80}")  # Clear any leftover text by padding with spaces
