class Display:
    def clear_screen(self):
        """Clear the terminal screen and reset the cursor."""
        print("\033[H\033[J", end="")  # Move cursor to the top-left and clear the screen

    def update_display(self, board, money, inventory, messages: list = []):
        self.clear_screen()
        board_rows = len(board)
        
        # Render the game board
        for i, row in enumerate(board):
            print(f"\033[{i + 1};1H", end="")  # Move to the specific row
            print(' '.join(row))
        
        # Render inventory and money status
        print(f"\033[{board_rows + 1};1H", end="")  # Move to the row below the board
        print(f"${money}             [{' '.join(inventory)}]")
        
        # Render additional messages
        for i, message in enumerate(messages):
            print(f"\033[{board_rows + 2 + i};1H", end="")  # Reserve rows for messages
            print(message)

        print("\n", end="")  # Ensure clean end of output