class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.floor_type = "metal_floor"
        self.wall = False
        self.object = None
        self.module = None

    def is_walkable(self):
        if self.wall:
            return False
        if self.object and getattr(self.object, 'solid', False):
            return False
        return True
