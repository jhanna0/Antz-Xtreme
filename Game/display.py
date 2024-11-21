from Pieces.character import Player
from Game.board import Board
from typing import List
from Game.broadcast import BroadCast

class Display:
    def __init__(self, board: Board):
        self.board = board
        self.messages: List[str] = []
        self.last_message = None  # Tracks the last unique message
        self.last_message_count = 0  # Tracks how many times the last message was repeated
        self._get_latest_board_size()
        BroadCast().subscribe(self)
    
    def _get_latest_board_size(self):
        self.board_rows = self.board.get_board_size()[0]

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
        """Clear the terminal screen and reset the cursor."""
        print("\033[H\033[J", end="")  # Move cursor to the top-left and clear the screen

    def update_display(self, player: Player):
        """Render the entire display, including the board, player info, and messages."""
        self.clear_screen()
        self._get_latest_board_size()

        # Render the game board
        for i, row in enumerate(self.board.get_board()):
            print(f"\033[{i + 1};1H", end="")  # Move to the specific row
            print(' '.join(row))
        
        print(f"\033[{self.board_rows + 1};1H", end="")  # Move to the row below the board
        print(f"${player.get_money()}             [{' '.join(player.inventory.get_items_symbols())}]")
        
        # Render additional messages
        self.update_messages()

    def update_messages(self):
        self._get_latest_board_size()
        for i, message in enumerate(self.messages):
            print(f"\033[{self.board_rows + 3 + i};1H", end="")  # Reserve rows for messages
            print(f"{message:<80}")  # Clear any leftover text by padding with spaces
