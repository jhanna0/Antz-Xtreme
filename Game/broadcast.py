class BroadCast:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.subscribers = []
        return cls._instance

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def announce(self, msg: str):
        for subscriber in self.subscribers:
            subscriber.add_message(msg)

broadcast = BroadCast()
