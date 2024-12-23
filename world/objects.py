class BaseObject:
    def __init__(self, name):
        self.name = name
        self.solid = False
        self.walkable = False

    def update(self, dt):
        pass

class Bed(BaseObject):
    def __init__(self):
        super().__init__("Bed")
        self.solid = True
        self.walkable = True

class StorageContainer(BaseObject):
    def __init__(self):
        super().__init__("Storage Container")
        self.solid = True
        self.walkable = False
