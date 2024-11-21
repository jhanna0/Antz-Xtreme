from Pieces.shop import Shop
from Managers.manager import Manager


class ShopManager(Manager[Shop]):
    def __init__(self):
        super().__init__()
