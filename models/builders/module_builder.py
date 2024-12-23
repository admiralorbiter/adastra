from .base_builder import BaseBuilder
from world.modules import (
    LifeSupportModule, 
    ReactorModule, 
    EngineModule,
    DockingDoorModule
)

class ModuleBuilder(BaseBuilder):
    def __init__(self, name: str, description: str, icon_color: tuple[int, int, int], module_type, cost: int = 10):
        super().__init__(name, description, icon_color, cost)
        self.module_type = module_type

    def can_build(self, ship, x: int, y: int) -> bool:
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
            
        tile = deck.tiles[y][x]
        
        # Special handling for DockingDoor
        if self.name == "Docking Door":
            # Try horizontal placement
            if x + 1 < deck.width:
                next_tile = deck.tiles[y][x + 1]
                if (tile.wall and next_tile.wall and 
                    not tile.module and not next_tile.module):
                    return True
                
            # Try vertical placement
            if y + 1 < deck.height:
                next_tile = deck.tiles[y + 1][x]
                if (tile.wall and next_tile.wall and 
                    not tile.module and not next_tile.module):
                    return True
            return False

        # Engine must be built on walls
        if self.name == "Engine":
            return tile.wall and not tile.module and not tile.object
            
        # Other modules can't be built on walls
        return not tile.wall and not tile.module and not tile.object

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        
        # Special handling for DockingDoor
        if self.name == "Docking Door":
            module = self.module_type()
            module.primary_position = (x, y)
            
            # Determine placement direction
            if x + 1 < deck.width and deck.tiles[y][x + 1].wall:
                module.direction = 'horizontal'
                module.secondary_position = (x + 1, y)
                deck.tiles[y][x + 1].module = module
            else:
                module.direction = 'vertical'
                module.secondary_position = (x, y + 1)
                deck.tiles[y + 1][x].module = module
            
            deck.tiles[y][x].module = module
            return True
        
        deck.tiles[y][x].module = self.module_type()
        return True 