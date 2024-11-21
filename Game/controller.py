from pynput import keyboard
import sys
import tty
import termios
import threading
from typing import Optional

from Game.definitions import Direction


class Controller:
    def __init__(self):
        self.last_input = None
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.exit_key = "p"
        self.running = True

    def listen(self):
        with InputSuppressor():
            with keyboard.Listener(on_press=self.handle_key_press) as listener:
                listener.join()

    def handle_key_press(self, key):
        try:
            self.last_input = key.char
        except AttributeError:  # Ignore special keys like Shift or Ctrl
            pass
    
    def process_latest_input(self) -> Optional[str]:
        key = self._get_last_input()
        if key == self.exit_key:
            self.stop()
        
        if key and key in self.move_list:
            return key

    def _get_last_input(self):
        """Return the last input and reset it."""
        key = self.last_input
        self.last_input = None
        return key

    def stop(self):
        self.running = False
        print("Stopping controller. Press CTRL+C to quit if stuck.")  # Help message if it hangs
    
    def start(self):
        threading.Thread(target = self.listen, daemon = True).start()


class InputSuppressor:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)  # Switch to raw mode to suppress input
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)  # Restore original settings
