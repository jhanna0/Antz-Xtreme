from typing import Callable, Dict, List, Any, Union
from Game.definitions import SignalType

class Signal:
    def __init__(self, type: Union[SignalType, str], data: Any = None):
        self.type = type
        self.data = data

class SignalManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.subscribers: Dict[str, List[Callable[[Signal], None]]] = {}
        return cls._instance

    def subscribe(self, signal_type: Union[SignalType, str], callback: Callable[[Signal], None]):
        key = str(signal_type)
        if key not in self.subscribers:
            self.subscribers[key] = []
        self.subscribers[key].append(callback)

    def emit(self, signal_type: Union[SignalType, str], data: Any = None):
        key = str(signal_type)
        if key in self.subscribers:
            signal = Signal(signal_type, data)
            for callback in self.subscribers[key]:
                try:
                    callback(signal)
                except Exception as e:
                    print(f"Error handling signal {key}: {e}")

signals = SignalManager()

