"""
Menu System - Terminal-based menu for ROM selection
"""
import os
import sys
from typing import List, Optional
from Game.rom_loader import ROMLoader, ROMMetadata


class Menu:
    """Terminal-based menu for selecting ROMs"""
    
    def __init__(self):
        self.rom_loader = ROMLoader()
        
    def reset_terminal(self):
        """Resets terminal to a clean state"""
        # Reset all terminal attributes
        sys.stdout.write('\033[0m')      # Reset colors/attributes
        sys.stdout.write('\033[?25h')    # Show cursor
        sys.stdout.write('\033[2J')      # Clear entire screen
        sys.stdout.write('\033[H')       # Move cursor to home position
        sys.stdout.flush()
        
    def clear_screen(self):
        """Clears the terminal screen"""
        # Use ANSI escape codes for better compatibility
        print('\033[2J\033[H', end='')
        sys.stdout.flush()
        
    def print_header(self):
        """Prints the game header"""
        print("\n" * 2)  # Add some spacing
        print("=" * 70)
        print("             ANTZ GAME ENGINE - ROM SELECTION")
        print("          Generic ASCII Adventure Game Engine")
        print("=" * 70)
        print()
        
    def print_rom_list(self, roms: List[ROMMetadata]):
        """Prints the available ROMs"""
        if not roms:
            print("No ROMs found in the ROMs directory.")
            print()
            return
            
        print("Available ROMs:")
        print()
        
        for i, rom in enumerate(roms, 1):
            print(f"  [{i}] {rom.name} v{rom.version}")
            print(f"      By: {rom.author}")
            print(f"      Difficulty: {rom.difficulty}")
            if rom.tags:
                print(f"      Tags: {', '.join(rom.tags)}")
            print(f"      {rom.description}")
            print()
            
    def show_menu(self) -> Optional[ROMMetadata]:
        """
        Displays the ROM selection menu and returns the selected ROM.
        Returns None if user wants to quit.
        """
        # Reset terminal state completely
        self.reset_terminal()
        
        # Give terminal a moment to reset
        import time
        time.sleep(0.1)
        
        self.print_header()
        
        # Scan for available ROMs
        roms = self.rom_loader.scan_roms()
        
        if not roms:
            print("ERROR: No ROMs found!")
            print("Please ensure ROMs are properly installed in the 'ROMs' directory.")
            input("Press Enter to exit...")
            return None
            
        self.print_rom_list(roms)
        
        print("-" * 70)
        print("  [Q] Quit")
        print("-" * 70)
        print()
        
        # Get user selection
        while True:
            choice = input("Select ROM number (or Q to quit): ").strip().lower()
            
            if choice == 'q':
                return None
                
            try:
                rom_index = int(choice) - 1
                if 0 <= rom_index < len(roms):
                    selected_rom = roms[rom_index]
                    print()
                    print(f"Loading: {selected_rom.name}...")
                    print()
                    return selected_rom
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(roms)}")
            except ValueError:
                print("Invalid input. Please enter a number or 'Q' to quit.")
                
    def show_error(self, message: str):
        """Displays an error message"""
        print()
        print("=" * 70)
        print(f"ERROR: {message}")
        print("=" * 70)
        print()

