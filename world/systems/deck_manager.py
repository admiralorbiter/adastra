from world.tile import Tile

class DeckManager:
    def __init__(self):
        self.decks = []

    def add_deck(self, deck):
        """Add a new deck to the ship"""
        self.decks.append(deck)

    def expand_deck(self, direction: str, x: int = None, y: int = None) -> None:
        """Handle deck expansion"""
        if not self.decks:
            return
        
        deck = self.decks[0]  # Currently only handling first deck
        
        def create_tile(x, y, is_wall=False):
            tile = Tile(x=x, y=y)
            tile.wall = is_wall
            return tile
        
        if direction == "right" and y is not None:
            self._expand_right(deck, y, create_tile)
        elif direction == "left" and y is not None:
            self._expand_left(deck, y, create_tile)
        elif direction == "down" and x is not None:
            self._expand_down(deck, x, create_tile)
        elif direction == "up" and x is not None:
            self._expand_up(deck, x, create_tile)

    def _expand_right(self, deck, y, create_tile):
        for row_idx, row in enumerate(deck.tiles):
            while len(row) <= deck.width:
                row.append(create_tile(len(row), row_idx))
        deck.tiles[y][deck.width] = create_tile(deck.width, y, is_wall=True)
        deck.width += 1

    def _expand_left(self, deck, y, create_tile):
        for row in deck.tiles:
            for tile in row:
                if tile:
                    tile.x += 1
            row.insert(0, create_tile(0, deck.tiles.index(row)))
        deck.tiles[y][0] = create_tile(0, y, is_wall=True)
        deck.width += 1

    def _expand_down(self, deck, x, create_tile):
        new_row = [create_tile(i, deck.height) for i in range(deck.width)]
        deck.tiles.append(new_row)
        deck.tiles[deck.height][x] = create_tile(x, deck.height, is_wall=True)
        deck.height += 1

    def _expand_up(self, deck, x, create_tile):
        for y in range(len(deck.tiles)):
            for tile in deck.tiles[y]:
                if tile:
                    tile.y += 1
        new_row = [create_tile(i, 0) for i in range(deck.width)]
        deck.tiles.insert(0, new_row)
        deck.tiles[0][x] = create_tile(x, 0, is_wall=True)
        deck.height += 1

    def calculate_oxygen_capacity(self) -> float:
        """Calculate total oxygen capacity based on floor tiles"""
        floor_tiles = 0
        for deck in self.decks:
            for y in range(deck.height):
                for x in range(deck.width):
                    if not deck.tiles[y][x].wall:
                        floor_tiles += 1
        return floor_tiles * 10  # 10 units of O2 per floor tile 