from world.tile import Tile


class Ship:
    def __init__(self, name="Unnamed Ship"):
        self.name = name
        self.decks = []
        self.global_oxygen = 100.0
        self.global_power = 0
        self.max_power = 0
        self.crew = []
        
        # New oxygen-related attributes
        self.oxygen_capacity = 100.0  # Maximum oxygen the ship can hold
        self.oxygen_consumption_per_crew = 0.1  # Oxygen used per crew member per second

    def add_deck(self, deck):
        self.decks.append(deck)

    def update(self, dt):
        # Update all decks and recalculate resources
        for deck in self.decks:
            deck.update(dt)
        
        # Update crew members with dt parameter
        for crew_member in self.crew:
            crew_member.update(dt)
            
        self.calculate_resources()

    def calculate_resources(self):
        total_power = 0
        life_support_oxygen = 0

        for deck in self.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module:
                        mod = tile.module
                        # Check module type
                        if hasattr(mod, 'power_output'):
                            total_power += mod.power_output
                        if hasattr(mod, 'oxygen_production'):
                            life_support_oxygen += mod.oxygen_production

        self.max_power = total_power
        self.global_oxygen += life_support_oxygen
        if self.global_oxygen > 100.0:
            self.global_oxygen = 100.0

        # Calculate oxygen changes
        total_oxygen_production = 0
        total_oxygen_consumption = len(self.crew) * self.oxygen_consumption_per_crew

        for deck in self.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module:
                        mod = tile.module
                        if hasattr(mod, 'oxygen_production'):
                            total_oxygen_production += mod.oxygen_production

        # Update oxygen levels
        oxygen_change = (total_oxygen_production - total_oxygen_consumption)
        self.global_oxygen = max(0.0, min(self.oxygen_capacity, self.global_oxygen + oxygen_change))

    def add_crew_member(self, crew_member):
        self.crew.append(crew_member)

    def expand_deck(self, direction: str) -> None:
        """Expand the deck in the specified direction"""
        if not self.decks:
            return
            
        deck = self.decks[0]
        new_tiles = []
        
        if direction == "right":
            # Add new column
            for y in range(deck.height):
                new_tile = Tile(x=deck.width, y=y)  # Use the new width as x coordinate
                new_tile.wall = True  # Start as wall
                deck.tiles[y].append(new_tile)
            deck.width += 1
            
        elif direction == "down":
            # Add new row
            new_row = [Tile(x=x, y=deck.height) for x in range(deck.width)]  # Use new height as y coordinate
            for tile in new_row:
                tile.wall = True  # Start as wall
            deck.tiles.append(new_row)
            deck.height += 1
