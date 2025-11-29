from typing import List, Callable
from Game.broadcast import broadcast
from Game.context import GameContext
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Pieces.machine import MoneyMachine
from Pieces.player import Player
from Pieces.source import Source
from Factory.factory import AbilityFactory
from Game.story import Story, Chapter
from Game.definitions import Direction, SignalType
from Game.signals import signals

# Managers & Core
from Game.generate import Generator
from Game.events import Events

class Tutorial(Chapter):
    def __init__(self, context: GameContext):
        super().__init__(name = "Welcome to Antz Island", objective = "Move Around")
        self.context = context
        self.starting_location = None

    def starting_action(self):
        super().starting_action()
        broadcast.announce("Use WASD to move around")
        self.starting_location = self.context.player.get_location()

    def completion_condition(self) -> bool:
        if self.starting_location is None:
            return False
        return self.context.player.get_location() != self.starting_location

    def completion_action(self):
        pass

class Chapter1(Chapter):
    def __init__(self, context: GameContext, kb_str: str, callback: Callable, factory: AbilityFactory):
        super().__init__(name = "Natural Resources", objective = "Pick up single resource")
        self.context = context
        self.kb_str = kb_str
        self.callback = callback
        self.factory = factory

    def starting_action(self):
        super().starting_action()
        broadcast.announce("Resources provide Value that grows the Queen")

    def completion_condition(self) -> bool:
        return len(self.context.player.inventory.get_items()) > 0

    def completion_action(self):
        broadcast.announce(f"Completed")
        self.callback(self.kb_str, self.factory.player_teleport())
        broadcast.announce("You've learned to teleport!")
        broadcast.announce("Press 'v' to teleport in the direction you're heading.")

class Chapter2(Chapter):
    def __init__(self, context: GameContext, kb_str: str, callback: Callable, factory: AbilityFactory):
        super().__init__(name = "Filling Up", objective = "Fill your inventory")
        self.context = context
        self.kb_str = kb_str
        self.callback = callback
        self.factory = factory

    def completion_condition(self):
        return self.context.player.inventory.is_inventory_full()

    def completion_action(self):
        broadcast.announce(f"Completed")
        self.callback(self.kb_str, self.factory.conjure_ability())
        broadcast.announce("You've learned to conjure!")
        broadcast.announce(f"Press '{self.kb_str}' to summon a helper robot.")

class Chapter3(Chapter):
    def __init__(self, context: GameContext, callback: Callable, factory: AbilityFactory):
        super().__init__(name = "Self Defense", objective = "Destroy a Source")
        self.context = context
        self.callback = callback
        self.factory = factory
        self.destroyed_count = 0
        self.subscribed = False

    def _handle_piece_removed(self, signal):
        piece = signal.data.get("piece")
        # We only care if a Source was destroyed
        # We can check type by class name or checking if it's in source manager
        if piece.__class__.__name__ == "Source":
            self.destroyed_count += 1

    def starting_action(self):
        super().starting_action()
        # Subscribe to piece removal
        if not self.subscribed:
            signals.subscribe(SignalType.PIECE_REMOVED, self._handle_piece_removed)
            self.subscribed = True

        broadcast.announce("You can now shoot projectiles!")
        broadcast.announce("Use I, J, K, L to shoot in directions.")
        
        # Register directional attacks
        self.callback("i", self.factory.directional_projectile(Direction.Up))
        self.callback("j", self.factory.directional_projectile(Direction.Left))
        self.callback("k", self.factory.directional_projectile(Direction.Down))
        self.callback("l", self.factory.directional_projectile(Direction.Right))

    def completion_condition(self):
        # Win if at least one source destroyed
        return self.destroyed_count > 0

    def completion_action(self):
        broadcast.announce("Target destroyed!")
        broadcast.announce("You are now ready for the real world.")

class Chapter4(Chapter):
    def __init__(self, context: GameContext, callback: Callable, factory: AbilityFactory):
        super().__init__(name = "Total Domination", objective = "Use Ultimate")
        self.context = context
        self.callback = callback
        self.factory = factory
        self.ultimate_used = False
        self.subscribed = False

    def _handle_ultimate_used(self, signal):
        # Assuming we add a signal for ability usage or check effect
        pass

    def starting_action(self):
        super().starting_action()
        broadcast.announce("You've unlocked your Ultimate ability!")
        broadcast.announce("Press 'u' to unleash a massive blast.")
        self.callback("u", self.factory.ultimate_ability())

    def completion_condition(self):
        # For simplicity, let's say they win if all sources are gone, which the ultimate does
        return len(self.context.get_entities(Source)) == 0

    def completion_action(self):
        broadcast.announce("The world is cleansed.")

class AntzStory(Story):
    def __init__(self, context: GameContext, kb_func: callable):
        super().__init__(name = "Antz Extreme")
        self.context = context
        self.chapters: List[Chapter] = []
        self.current_chapter_index = 0
        self.factory = AbilityFactory(self.context)

        self.add_chapter(
            Tutorial(
                context = self.context
            )
        )
        self.add_chapter(
            Chapter1(
                context = self.context,
                kb_str = "v",
                callback = kb_func,
                factory = self.factory
            )
        )
        self.add_chapter(
            Chapter2(
                context = self.context,
                kb_str = "c",
                callback = kb_func,
                factory = self.factory
            )
        )
        self.add_chapter(
             Chapter3(
                 context = self.context,
                 callback = kb_func,
                 factory = self.factory
             )
        )
        self.add_chapter(
             Chapter4(
                 context = self.context,
                 callback = kb_func,
                 factory = self.factory
             )
        )
    
    def setup(self, game):
        board = self.context.board
        
        # Core managers are now unified in EntityManager,
        # but we can still register special logic or just let the Story
        # handle creation. For this refactor, we rely on the GameContext's
        # internal EntityManager.
        
        # Setup Generator and Events
        # Generator needs to know how to create sources. 
        # We pass the entity manager for registration.
        # We also inject generation config into the entity manager or generator
        
        # Injection of config for generator
        self.context.entity_manager.potential_sources = (97, 123)
        
        generator = Generator(board, self.context.entity_manager)
        events = Events(generator)
        
        self.context.generator = generator
        self.context.events = events
        
        # Setup Player
        player = Player(
            symbol = "~",
            location = generator.find_location_for_piece()
        )
        self.context.player = player
        self.context.register_entity(player)
        
        # Register Player in Game (if needed by Game logic outside context)
        if hasattr(game, 'set_player'):
            game.set_player(player)

    def start(self):
        super().start()
        # Register entities
        self.context.register_entity(
            MoneyMachine(
                symbol = "$",
                location = self.context.generator.find_location_for_piece(edge_preference = True)
            )
        )
        self.context.register_entity(
            Shop(
                context = self.context,
                piece_type = MinerRobot,
                location = self.context.generator.find_location_for_piece(edge_preference=True)
            )
        )
    
    def every_turn(self):
        self.context.events.random_event()
