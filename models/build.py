from enum import Enum, auto
from dataclasses import dataclass

from world.modules import LifeSupportModule, ReactorModule, EngineModule
from world.objects import Bed, StorageContainer, Tank
from world.tile import Tile

class BuildMode(Enum):
    NONE = auto()
    FLOOR = auto()
    WALL = auto()
    CABLE = auto()
    OBJECT = auto()
    MODULE = auto()

@dataclass
class BuildableItem:
    name: str
    description: str
    icon_color: tuple[int, int, int]  # RGB color tuple
    cost: int = 10
    
    def can_build(self, ship, x: int, y: int) -> bool:
        """Check if item can be built at the specified location"""
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        # For floor and wall, allow building within bounds or one tile beyond
        if self.name in ["Basic Floor", "Basic Wall"]:
            # Allow building one tile beyond in any direction
            if not (-1 <= x <= deck.width and -1 <= y <= deck.height):
                return False
            
            # If within bounds, check if tile is empty or (for floor) is a wall
            if 0 <= x < deck.width and 0 <= y < deck.height:
                tile = deck.tiles[y][x]
                if self.name == "Basic Floor":
                    # Can place floor on wall tiles
                    if tile.module or tile.object:
                        return False
                else:  # Basic Wall
                    if tile.wall or tile.module or tile.object:
                        return False
                
            # Must be adjacent to existing tile
            adjacent_coords = [
                (ax, ay) for ax, ay in [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1)
                ] if 0 <= ax < deck.width and 0 <= ay < deck.height
            ]
            
            # For floor, must be adjacent to existing floor or wall
            if self.name == "Basic Floor":
                return any(not deck.tiles[ay][ax].wall for ax, ay in adjacent_coords)
            # For wall, just needs to be adjacent to any tile
            return len(adjacent_coords) > 0
        
        # Special handling for Engine - must be built on walls
        if self.name == "Engine":
            if not (0 <= x < deck.width and 0 <= y < deck.height):
                return False
            tile = deck.tiles[y][x]
            # Check if tile is a wall and doesn't have any other modules
            return tile.wall and not tile.module and not tile.object
        
        # For other items, check normal bounds
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
        
        # Other modules can't be built on walls
        tile = deck.tiles[y][x]
        if tile.wall:
            return False
        
        return True

    def build(self, ship, x: int, y: int) -> bool:
        """Actually perform the building action"""
        # Convert screen coordinates to grid coordinates
        grid_x = int(x)  # Already converted in UI
        grid_y = int(y)  # Already converted in UI
        
        if not self.can_build(ship, grid_x, grid_y):
            return False
            
        deck = ship.decks[0]
        
        # Handle module placement
        if self.name == "Life Support":
            deck.tiles[grid_y][grid_x].module = LifeSupportModule()
            return True
        elif self.name == "Reactor":
            deck.tiles[grid_y][grid_x].module = ReactorModule()
            return True
        elif self.name == "Engine":
            deck.tiles[grid_y][grid_x].module = EngineModule()
            return True
        
        # Handle wall placement with expansion
        if self.name == "Basic Wall":
            # Handle expansion cases
            if grid_x == deck.width:
                ship.expand_deck("right", y=grid_y)
                return True
            elif grid_x == -1:
                ship.expand_deck("left", y=grid_y)
                return True
            elif grid_y == deck.height:
                ship.expand_deck("down", x=grid_x)
                return True
            elif grid_y == -1:
                ship.expand_deck("up", x=grid_x)
                return True
            
            # Place single wall within bounds
            if 0 <= grid_x < deck.width and 0 <= grid_y < deck.height:
                # Ensure tile exists before setting wall
                if not deck.tiles[grid_y][grid_x]:
                    deck.tiles[grid_y][grid_x] = Tile(x=grid_x, y=grid_y)
                deck.tiles[grid_y][grid_x].wall = True
                return True
        
        # Handle object placement
        if self.name == "Storage Tank":
            deck.tiles[grid_y][grid_x].object = Tank()
            return True
        elif self.name == "Storage Container":
            deck.tiles[grid_y][grid_x].object = StorageContainer()
            return True
        elif self.name == "Bed":
            deck.tiles[grid_y][grid_x].object = Bed()
            return True
        
        # Handle floor placement with automatic wall creation
        elif self.name == "Basic Floor":
            if not deck.tiles[grid_y][grid_x]:
                deck.tiles[grid_y][grid_x] = Tile(x=grid_x, y=grid_y)
            deck.tiles[grid_y][grid_x].wall = False
            
            # Check for needed expansion in each direction
            if grid_x == deck.width - 1:  # Right edge
                ship.expand_deck("right", y=grid_y)
            elif grid_x == 0:  # Left edge
                ship.expand_deck("left", y=grid_y)
            
            if grid_y == deck.height - 1:  # Bottom edge
                ship.expand_deck("down", x=grid_x)
            elif grid_y == 0:  # Top edge
                ship.expand_deck("up", x=grid_x)
            
            # Create walls in empty space around the edges of the ship
            for y in range(deck.height):
                if not deck.tiles[y][0].wall and not deck.tiles[y][0].module and not deck.tiles[y][0].object:
                    deck.tiles[y][0].wall = True
                if not deck.tiles[y][deck.width-1].wall and not deck.tiles[y][deck.width-1].module and not deck.tiles[y][deck.width-1].object:
                    deck.tiles[y][deck.width-1].wall = True
            
            for x in range(deck.width):
                if not deck.tiles[0][x].wall and not deck.tiles[0][x].module and not deck.tiles[0][x].object:
                    deck.tiles[0][x].wall = True
                if not deck.tiles[deck.height-1][x].wall and not deck.tiles[deck.height-1][x].module and not deck.tiles[deck.height-1][x].object:
                    deck.tiles[deck.height-1][x].wall = True
            
            return True
        elif self.name == "Power Cable":
            ship.cable_system.add_cable(grid_x, grid_y)
            return True
        
        return False

class BuildCategory:
    def __init__(self, mode: BuildMode, items: list[BuildableItem]):
        self.mode = mode
        self.items = items
        self.selected_item: BuildableItem | None = None

class BuildSystem:
    def __init__(self):
        self.current_mode = BuildMode.NONE
        self.categories = {
            BuildMode.FLOOR: BuildCategory(BuildMode.FLOOR, [
                BuildableItem("Basic Floor", "A simple metal floor", (200, 200, 200)),
            ]),
            BuildMode.WALL: BuildCategory(BuildMode.WALL, [
                BuildableItem("Basic Wall", "Standard wall panel", (100, 100, 100)),
            ]),
            BuildMode.CABLE: BuildCategory(BuildMode.CABLE, [
                BuildableItem("Power Cable", "Basic power cable", (255, 140, 0)),
            ]),
            BuildMode.OBJECT: BuildCategory(BuildMode.OBJECT, [
                BuildableItem("Bed", "A place for crew to rest", (139, 69, 19)),
                BuildableItem("Storage Container", "Store items and resources", (160, 82, 45)),
                BuildableItem("Storage Tank", "Store liquids and gases", (0, 191, 255))
            ]),
            BuildMode.MODULE: BuildCategory(BuildMode.MODULE, [
                BuildableItem("Life Support", "Generates oxygen for the ship", (100, 100, 255)),
                BuildableItem("Reactor", "Generates power for the ship", (255, 140, 0)),
                BuildableItem("Engine", "Provides thrust for ship movement", (50, 255, 50))
            ])
        }
        self.active_category: BuildCategory | None = None

    def set_mode(self, mode: BuildMode) -> None:
        if self.current_mode == mode:
            self.current_mode = BuildMode.NONE
            self.active_category = None
        else:
            self.current_mode = mode
            self.active_category = self.categories.get(mode)
            if self.active_category:
                self.active_category.selected_item = self.active_category.items[0]

    def get_current_item(self) -> BuildableItem | None:
        if self.active_category:
            return self.active_category.selected_item
        return None 