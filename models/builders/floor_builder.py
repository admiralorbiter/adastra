from .base_builder import BaseBuilder
from world.tile import Tile

class FloorBuilder(BaseBuilder):
    def can_build(self, ship, x: int, y: int) -> bool:
        if not ship.decks:
            return False
        deck = ship.decks[0]
        
        # Allow building within bounds or one tile beyond
        if not (-1 <= x <= deck.width and -1 <= y <= deck.height):
            return False
            
        # If within bounds, check if tile is empty or is a wall
        if 0 <= x < deck.width and 0 <= y < deck.height:
            tile = deck.tiles[y][x]
            if tile.module or tile.object:
                return False
                
        # Must be adjacent to existing floor
        adjacent_coords = [
            (ax, ay) for ax, ay in [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1)
            ] if 0 <= ax < deck.width and 0 <= ay < deck.height
        ]
        return any(not deck.tiles[ay][ax].wall for ax, ay in adjacent_coords)

    def build(self, ship, x: int, y: int) -> bool:
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        
        # Create floor tile
        if not deck.tiles[y][x]:
            deck.tiles[y][x] = Tile(x=x, y=y)
        deck.tiles[y][x].wall = False
        
        # Handle expansion if needed
        if x == deck.width - 1:  # Right edge
            ship.deck_manager.expand_deck("right", y=y)
        elif x == 0:  # Left edge
            ship.deck_manager.expand_deck("left", y=y)
        
        if y == deck.height - 1:  # Bottom edge
            ship.deck_manager.expand_deck("down", x=x)
        elif y == 0:  # Top edge
            ship.deck_manager.expand_deck("up", x=x)
        
        # Create walls in empty space around edges
        self._update_edge_walls(deck)
        return True

    def _update_edge_walls(self, deck):
        """Create walls in empty space around the edges of the ship"""
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