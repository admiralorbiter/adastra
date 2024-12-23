from enum import Enum, auto
from dataclasses import dataclass

from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
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
        
        # For wall, allow building within bounds or one tile beyond
        if self.name == "Basic Wall":
            # Allow building one tile beyond in any direction
            if not (-1 <= x <= deck.width and -1 <= y <= deck.height):
                return False
            
            # If within bounds, check if tile is empty
            if 0 <= x < deck.width and 0 <= y < deck.height:
                tile = deck.tiles[y][x]
                if tile.wall or tile.module or tile.object:
                    return False
                
            # Must be adjacent to existing tile
            adjacent_coords = [
                (ax, ay) for ax, ay in [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1)
                ] if 0 <= ax < deck.width and 0 <= ay < deck.height
            ]
            return len(adjacent_coords) > 0
        
        # For other items, check normal bounds
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
        
        return True

    def build(self, ship, x: int, y: int) -> bool:
        """Actually perform the building action"""
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        
        # Handle module placement
        if self.name == "Life Support":
            deck.tiles[y][x].module = LifeSupportModule()
            return True
        elif self.name == "Reactor":
            deck.tiles[y][x].module = ReactorModule()
            return True
        
        # Handle wall placement with expansion
        if self.name == "Basic Wall":
            # Handle expansion cases
            if x == deck.width:
                ship.expand_deck("right", y=y)
                return True
            elif x == -1:
                ship.expand_deck("left", y=y)
                return True
            elif y == deck.height:
                ship.expand_deck("down", x=x)
                return True
            elif y == -1:
                ship.expand_deck("up", x=x)
                return True
            
            # Place single wall within bounds
            if 0 <= x < deck.width and 0 <= y < deck.height:
                # Ensure tile exists before setting wall
                if not deck.tiles[y][x]:
                    deck.tiles[y][x] = Tile(x=x, y=y)
                deck.tiles[y][x].wall = True
                return True
        
        # Handle other building types...
        elif self.name == "Basic Floor":
            if not deck.tiles[y][x]:
                deck.tiles[y][x] = Tile(x=x, y=y)
            deck.tiles[y][x].wall = False
            return True
        elif self.name == "Bed":
            deck.tiles[y][x].object = Bed()
            return True
        elif self.name == "Storage Container":
            deck.tiles[y][x].object = StorageContainer()
            return True
        elif self.name == "Power Cable":
            ship.cable_system.add_cable(x, y)
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
                BuildableItem("Storage Container", "Store items and resources", (160, 82, 45))
            ]),
            BuildMode.MODULE: BuildCategory(BuildMode.MODULE, [
                BuildableItem("Life Support", "Generates oxygen for the ship", (100, 100, 255)),
                BuildableItem("Reactor", "Generates power for the ship", (255, 140, 0))
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