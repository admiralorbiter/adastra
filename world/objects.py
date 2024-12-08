class BaseObject:
    def __init__(self, name):
        self.name = name
        self.solid = False

    def update(self, dt):
        pass

class Bed(BaseObject):
    def __init__(self):
        super().__init__("Bed")
        self.solid = True

class StorageContainer(BaseObject):
    def __init__(self):
        super().__init__("Storage Container")
        self.solid = True
