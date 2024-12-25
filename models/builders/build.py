from enum import Enum, auto
from dataclasses import dataclass

from models.builders.object_builder import ObjectBuilder
from world.modules import (
    LifeSupportModule, 
    ReactorModule, 
    EngineModule,
    DockingDoorModule
)
from world.objects import Bed, StorageContainer, Tank
from world.tile import Tile
from world.weapons import LaserTurret

class BuildMode(Enum):
    NONE = auto()
    FLOOR = auto()
    WALL = auto()
    CABLE = auto()
    OBJECT = auto()
    MODULE = auto()
    WEAPON = auto()

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
        
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
        
        tile = deck.tiles[y][x]
        
        # Special handling for Engine and DockingDoor - must be built on walls
        if self.name in ["Engine", "Docking Door"]:
            if not tile.wall or tile.module or tile.object:
                return False
            
            # Additional check for DockingDoor - needs two adjacent walls
            if self.name == "Docking Door":
                # Check horizontal placement
                if x + 1 < deck.width:
                    next_tile = deck.tiles[y][x + 1]
                    if next_tile.wall and not next_tile.module:
                        return True
                # Check vertical placement
                if y + 1 < deck.height:
                    next_tile = deck.tiles[y + 1][x]
                    if next_tile.wall and not next_tile.module:
                        return True
                return False
            
            return True
        
        # Other modules can't be built on walls
        return not tile.wall and not tile.module and not tile.object

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
        elif self.name == "Docking Door":
            module = DockingDoorModule()
            module.primary_position = (grid_x, grid_y)
            
            # Check horizontal placement
            if grid_x + 1 < deck.width and deck.tiles[grid_y][grid_x + 1].wall:
                module.direction = 'horizontal'
                module.secondary_position = (grid_x + 1, grid_y)
                deck.tiles[grid_y][grid_x].module = module
                deck.tiles[grid_y][grid_x + 1].module = module
                return True
            # Check vertical placement    
            elif grid_y + 1 < deck.height and deck.tiles[grid_y + 1][grid_x].wall:
                module.direction = 'vertical'
                module.secondary_position = (grid_x, grid_y + 1)
                deck.tiles[grid_y][grid_x].module = module
                deck.tiles[grid_y + 1][grid_x].module = module
                return True
            return False
        
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
        
        # Add Laser Turret placement
        elif self.name == "Laser Turret":
            deck = ship.decks[0]  # Get main deck
            if 0 <= grid_x < deck.width and 0 <= grid_y < deck.height:
                turret = LaserTurret()
                deck.tiles[grid_y][grid_x].object = turret
                turret.tile = deck.tiles[grid_y][grid_x]
                turret.x = grid_x
                turret.y = grid_y
                turret.set_ship(ship)  # Important: Set the ship reference
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
                BuildableItem("Engine", "Provides thrust for ship movement", (50, 255, 50)),
                BuildableItem("Docking Door", "Allows ships to dock when powered", (150, 150, 150))
            ]),
            BuildMode.WEAPON: BuildCategory(BuildMode.WEAPON, [
                BuildableItem("Laser Turret", "Automated defense weapon", (255, 0, 0))
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
                if mode == BuildMode.WEAPON:
                    # For weapons, set the selected item when mode is changed
                    self.active_category.selected_item = self.active_category.items[0]
                else:
                    self.active_category.selected_item = self.active_category.items[0]

    def get_current_item(self) -> BuildableItem | None:
        if self.active_category:
            return self.active_category.selected_item
        return None 

    def clear_selection(self):
        """Clear the current build mode and selection"""
        self.current_mode = BuildMode.NONE
        self.active_category = None
        # Deactivate all category selections
        for category in self.categories.values():
            category.selected_item = None 