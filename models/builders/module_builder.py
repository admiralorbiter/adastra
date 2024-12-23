from .base_builder import BaseBuilder
from world.modules import LifeSupportModule, ReactorModule, EngineModule

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
        
        # Engine must be built on walls
        if self.name == "Engine":
            return tile.wall and not tile.module and not tile.object
            
        # Other modules can't be built on walls
        return not tile.wall and not tile.module and not tile.object

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        deck.tiles[y][x].module = self.module_type()
        return True 