from .tile import Tile

class Deck:
    def __init__(self, width, height, name="Deck"):
        self.name = name
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y) for x in range(width)] for y in range(height)]
        self.rooms = []

    def update(self, dt):
        # Update each room, and indirectly tiles/modules/objects
        for room in self.rooms:
            room.update(dt)
