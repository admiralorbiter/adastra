from world.objects import StorageContainer
from world.systems.resource_manager import ResourceManager
from world.systems.inventory_system import InventorySystem
from world.systems.crew_manager import CrewManager
from world.systems.deck_manager import DeckManager

class Ship:
    def __init__(self, name="Unnamed Ship"):
        self.name = name
        self.cable_system = None
        
        # Initialize systems
        self.resource_manager = ResourceManager()
        self.inventory_system = InventorySystem()
        self.inventory_system.ship = self
        self.crew_manager = CrewManager()
        self.deck_manager = DeckManager()

    # Properties to maintain backward compatibility
    @property
    def global_oxygen(self):
        return self.resource_manager.global_oxygen

    @property
    def global_power(self):
        return self.resource_manager.global_power

    @property
    def max_power(self):
        return self.resource_manager.max_power

    @property
    def oxygen_capacity(self):
        return self.resource_manager.oxygen_capacity

    @property
    def oxygen_consumption_per_crew(self):
        return self.resource_manager.oxygen_consumption_per_crew

    @property
    def decks(self):
        return self.deck_manager.decks

    @property
    def crew(self):
        return self.crew_manager.crew

    def calculate_oxygen_capacity(self):
        """Delegate to deck manager's calculate_oxygen_capacity"""
        oxygen_capacity = self.deck_manager.calculate_oxygen_capacity()
        self.resource_manager.oxygen_capacity = oxygen_capacity
        self.resource_manager.global_oxygen = oxygen_capacity

    def update(self, dt):
        """Update ship systems"""
        if dt == 0:  # Skip updates when paused
            return
            
        # Update all systems
        for deck in self.decks:
            deck.update(dt)
        
        self.crew_manager.update(dt)
        if self.cable_system:
            self.cable_system.update_networks()
        self.resource_manager.update(dt, self)

    def add_deck(self, deck):
        """Add a new deck to the ship"""
        self.deck_manager.add_deck(deck)
        self.calculate_oxygen_capacity()
        
        # Register all storage containers in the deck
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                if tile.object and isinstance(tile.object, StorageContainer):
                    self.inventory_system.register_container(tile.object)

    def add_crew_member(self, crew_member):
        """Add a new crew member to the ship"""
        self.crew_manager.add_crew_member(crew_member, self)

    def expand_deck(self, direction: str, x: int = None, y: int = None):
        """Expand the ship's deck"""
        self.deck_manager.expand_deck(direction, x, y)
        self.calculate_oxygen_capacity()

    def add_tank(self, tank):
        """Add a new resource tank"""
        self.resource_manager.add_tank(tank)

    def get_total_food(self):
        """Get total food in storage"""
        return self.inventory_system.get_total_food()

    def find_nearest_storage(self, x: int, y: int):
        """Find nearest storage container with food"""
        return self.inventory_system.find_nearest_storage(x, y)
