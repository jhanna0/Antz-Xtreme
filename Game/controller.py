from pynput import keyboard
import sys
import tty
import termios
from enum import Enum

class Controller:
    def __init__(self):
        self.last_input = None
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.exit_key = "p"
        self.running = True

    def handle_key_press(self, key):
        """Store the last pressed key."""
        try:
            self.last_input = key.char

        except AttributeError:
            pass  # Ignore special keys like Shift or Ctrl

    def listen(self):
        """Start listening for keyboard input with input suppression."""
        with InputSuppressor():
            with keyboard.Listener(on_press=self.handle_key_press) as listener:
                listener.join()

    def get_last_input(self):
        """Return the last input and reset it."""
        key = self.last_input
        self.last_input = None
        return key

    def stop(self):
        """Stop the input listener."""
        self.running = False
        print("Stopping controller. Press CTRL+C to quit if stuck.")  # Help message if it hangs
    
    def get_exit_key(self):
        return self.exit_key


class InputSuppressor:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)  # Switch to raw mode to suppress input
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)  # Restore original settings
