from .base_builder import BaseBuilder

class CableBuilder(BaseBuilder):
    def can_build(self, ship, x: int, y: int) -> bool:
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
            
        tile = deck.tiles[y][x]
        return not tile.wall

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        ship.cable_system.add_cable(x, y)
        return True 