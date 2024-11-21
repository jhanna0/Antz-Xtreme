from Pieces.machine import Machine
from Managers.manager import Manager


class MachineManager(Manager[Machine]):
    def __init__(self):
        super().__init__()
