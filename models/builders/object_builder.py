from .base_builder import BaseBuilder
from world.objects import Bed, StorageContainer, Tank

class ObjectBuilder(BaseBuilder):
    def __init__(self, name: str, description: str, icon_color: tuple[int, int, int], object_type, cost: int = 10):
        super().__init__(name, description, icon_color, cost)
        self.object_type = object_type

    def can_build(self, ship, x: int, y: int) -> bool:
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
            
        tile = deck.tiles[y][x]
        return not tile.wall and not tile.module and not tile.object

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        deck.tiles[y][x].object = self.object_type()
        return True 