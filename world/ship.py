from world.tile import Tile


class Ship:
    def __init__(self, name="Unnamed Ship"):
        self.name = name
        self.decks = []
        self.global_oxygen = 100.0
        self.global_power = 0
        self.max_power = 0
        self.crew = []
        self.cable_system = None
        
        # New oxygen-related attributes
        self.oxygen_capacity = 100.0  # Maximum oxygen the ship can hold
        self.oxygen_consumption_per_crew = 0.1  # Oxygen used per crew member per second

    def add_deck(self, deck):
        self.decks.append(deck)
        self.calculate_oxygen_capacity()

    def update(self, dt):
        # Update all decks and recalculate resources
        for deck in self.decks:
            deck.update(dt)
        
        # Update crew members with dt parameter
        for crew_member in self.crew:
            crew_member.update(dt)
            
        # Update cable system and power distribution
        self.cable_system.update_networks()
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
        if self.global_oxygen > self.oxygen_capacity:
            self.global_oxygen = self.oxygen_capacity

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

    def expand_deck(self, direction: str, x: int = None, y: int = None) -> None:
        if not self.decks:
            return
        
        deck = self.decks[0]
        
        def create_tile(x, y, is_wall=False):
            tile = Tile(x=x, y=y)
            tile.wall = is_wall
            return tile
        
        if direction == "right" and y is not None:
            # Ensure all rows have proper width first
            for row_idx, row in enumerate(deck.tiles):
                while len(row) <= deck.width:
                    row.append(create_tile(len(row), row_idx))
            # Add wall tile
            deck.tiles[y][deck.width] = create_tile(deck.width, y, is_wall=True)
            deck.width += 1
            self.calculate_oxygen_capacity()
            
        elif direction == "left" and y is not None:
            # Shift all x coordinates right
            for row in deck.tiles:
                for tile in row:
                    if tile:
                        tile.x += 1
                # Insert empty tiles at start of each row
                row.insert(0, create_tile(0, deck.tiles.index(row)))
            # Add wall tile
            deck.tiles[y][0] = create_tile(0, y, is_wall=True)
            deck.width += 1
            self.calculate_oxygen_capacity()
            
        elif direction == "down" and x is not None:
            # Add new row with proper tiles
            new_row = [create_tile(i, deck.height) for i in range(deck.width)]
            deck.tiles.append(new_row)
            # Set wall tile
            deck.tiles[deck.height][x] = create_tile(x, deck.height, is_wall=True)
            deck.height += 1
            self.calculate_oxygen_capacity()
            
        elif direction == "up" and x is not None:
            # Shift all y coordinates down
            for y in range(len(deck.tiles)):
                for tile in deck.tiles[y]:
                    if tile:
                        tile.y += 1
            # Add new row with proper tiles
            new_row = [create_tile(i, 0) for i in range(deck.width)]
            deck.tiles.insert(0, new_row)
            # Set wall tile
            deck.tiles[0][x] = create_tile(x, 0, is_wall=True)
            deck.height += 1
            self.calculate_oxygen_capacity()

    def calculate_oxygen_capacity(self):
        floor_tiles = 0
        for deck in self.decks:
            for y in range(deck.height):
                for x in range(deck.width):
                    if not deck.tiles[y][x].wall:
                        floor_tiles += 1
        # Each floor tile contributes to oxygen capacity
        self.oxygen_capacity = floor_tiles * 10  # 10 units of O2 per floor tile
        self.global_oxygen = self.oxygen_capacity  # Start with full O2
