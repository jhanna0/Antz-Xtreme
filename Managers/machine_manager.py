from Managers.manager import Manager

class MachineManager(Manager):
    def __init__(self):
        super().__init__()

    # not being used but I think it should
    # def calculate_player_interaction(self, player: Player):
    #     for machine in self.machines.values():
    #         if player.get_location() == machine.get_location():
    #             inv = player.get_inventory()
    #             if inv:
    #                 item = inv.pop()
    #                 player.add_money(machine.convert(item))
    #                 BroadCast().announce(f"You sold {item.get_symbol()} for {item.get_worth()}")
