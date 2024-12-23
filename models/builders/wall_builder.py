from .base_builder import BaseBuilder
from world.tile import Tile

class WallBuilder(BaseBuilder):
    def can_build(self, ship, x: int, y: int) -> bool:
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        # Allow building within bounds or one tile beyond
        if not (-1 <= x <= deck.width and -1 <= y <= deck.height):
            return False
            
        # If within bounds, check if tile is empty
        if 0 <= x < deck.width and 0 <= y < deck.height:
            tile = deck.tiles[y][x]
            if tile.wall or tile.module or tile.object:
                return False
                
        # Must be adjacent to any existing tile
        adjacent_coords = [
            (ax, ay) for ax, ay in [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1)
            ] if 0 <= ax < deck.width and 0 <= ay < deck.height
        ]
        return len(adjacent_coords) > 0

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        
        # Handle expansion cases
        if x == deck.width:
            ship.deck_manager.expand_deck("right", y=y)
            return True
        elif x == -1:
            ship.deck_manager.expand_deck("left", y=y)
            return True
        elif y == deck.height:
            ship.deck_manager.expand_deck("down", x=x)
            return True
        elif y == -1:
            ship.deck_manager.expand_deck("up", x=x)
            return True
        
        # Place single wall within bounds
        if 0 <= x < deck.width and 0 <= y < deck.height:
            if not deck.tiles[y][x]:
                deck.tiles[y][x] = Tile(x=x, y=y)
            deck.tiles[y][x].wall = True
            return True
            
        return False 