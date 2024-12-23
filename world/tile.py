class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.floor_type = "metal_floor"
        self.wall = False
        self.object = None
        self.module = None
        self.cable = None
        self.connected_modules = set()  # Track connected modules through cables

    def is_walkable(self):
        # Base tiles are walkable if they're not walls
        if self.wall:
            return False
        # Objects might block movement unless they're walkable
        if self.object and self.object.solid and not self.object.walkable:
            return False
        return True
