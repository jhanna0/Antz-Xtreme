from Game.signals import signals, SignalType

class BroadCast:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def subscribe(self, subscriber):
        # Deprecated: Subscribers should subscribe to signals directly
        pass

    def announce(self, msg: str):
        signals.emit(SignalType.MESSAGE, msg)

# maybe the only fine example of singleton
broadcast = BroadCast()
