class Room:
    def __init__(self, tiles):
        self.tiles = tiles  # A list of Tile instances

    def update(self, dt):
        for tile in self.tiles:
            if tile.module:
                tile.module.update(dt)
            if tile.object:
                tile.object.update(dt)
