from world.items import ItemType
from world.objects import StorageContainer, Tank
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
        self.oxygen_consumption_per_crew = 1  # Oxygen used per crew member per second
        self.oxygen_tanks = []  # List to store oxygen tanks
        self.water_tanks = []   # List to store water tanks
        
    def add_deck(self, deck):
        self.decks.append(deck)
        self.calculate_oxygen_capacity()

    def update(self, dt):
        if dt == 0:  # Skip updates when paused
            return
            
        # Update all decks and recalculate resources
        for deck in self.decks:
            deck.update(dt)
        
        # Update crew members with dt parameter
        for crew_member in self.crew:
            crew_member.update(dt)
            
        # Update cable system and power distribution
        self.cable_system.update_networks()
        self.calculate_resources(dt)  # Pass dt to calculate_resources
        
    def calculate_resources(self, dt):
        total_power = 0
        life_support_oxygen = 0

        for deck in self.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module:
                        mod = tile.module
                        if hasattr(mod, 'power_output'):
                            total_power += mod.power_output
                        if hasattr(mod, 'oxygen_production'):
                            life_support_oxygen += mod.oxygen_production * dt

        self.max_power = total_power
        
        # Calculate oxygen changes with dt
        total_oxygen_production = life_support_oxygen
        total_oxygen_consumption = len(self.crew) * self.oxygen_consumption_per_crew * dt

        # Update oxygen levels
        oxygen_change = (total_oxygen_production - total_oxygen_consumption)
        self.global_oxygen = max(0.0, min(self.oxygen_capacity, self.global_oxygen + oxygen_change))

        # Update resources in tanks
        if oxygen_change > 0:
            # Add oxygen to tanks
            remaining_oxygen = oxygen_change
            for deck in self.decks:
                for y in range(deck.height):
                    for x in range(deck.width):
                        tile = deck.tiles[y][x]
                        if tile.object and isinstance(tile.object, Tank):
                            remaining_oxygen = tile.object.add_resource(ItemType.OXYGEN, remaining_oxygen)
                            if remaining_oxygen <= 0:
                                break
        else:
            # Remove oxygen from tanks
            needed_oxygen = -oxygen_change
            for deck in self.decks:
                for y in range(deck.height):
                    for x in range(deck.width):
                        tile = deck.tiles[y][x]
                        if tile.object and isinstance(tile.object, Tank):
                            needed_oxygen -= tile.object.remove_resource(ItemType.OXYGEN, needed_oxygen)
                            if needed_oxygen <= 0:
                                break

    def add_crew_member(self, crew_member):
        crew_member.ship = self  # Set the ship reference
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

    def get_total_food(self):
        total_food = 0
        for deck in self.decks:
            for y in range(deck.height):
                for x in range(deck.width):
                    tile = deck.tiles[y][x]
                    if tile.object and isinstance(tile.object, StorageContainer):
                        total_food += tile.object.get_item_count(ItemType.FOOD)
        return total_food

    def find_nearest_storage(self, x: int, y: int) -> tuple[StorageContainer, tuple[int, int]] | None:
        """Find nearest storage container with food and its position"""
        nearest_distance = float('inf')
        nearest_storage = None
        nearest_pos = None
        
        for deck in self.decks:
            for tile_y in range(deck.height):
                for tile_x in range(deck.width):
                    tile = deck.tiles[tile_y][tile_x]
                    if (tile.object and isinstance(tile.object, StorageContainer) 
                        and tile.object.get_item_count(ItemType.FOOD) > 0):
                        distance = ((tile_x - x) ** 2 + (tile_y - y) ** 2) ** 0.5
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_storage = tile.object
                            nearest_pos = (tile_x, tile_y)
        
        return (nearest_storage, nearest_pos) if nearest_storage else None

    def add_tank(self, tank: Tank):
        if tank.resource_type == ItemType.OXYGEN:
            self.oxygen_tanks.append(tank)
        elif tank.resource_type == ItemType.WATER:
            self.water_tanks.append(tank)

    def get_total_oxygen(self) -> float:
        return sum(tank.current_amount for tank in self.oxygen_tanks)

    def get_total_oxygen_capacity(self) -> float:
        return sum(tank.capacity for tank in self.oxygen_tanks)

    def get_total_water(self) -> float:
        return sum(tank.current_amount for tank in self.water_tanks)
