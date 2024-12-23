from world.items import Item, ItemType

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
        self.items = []  # List to store items
        self.capacity = 100  # Maximum number of items
        
    def add_item(self, item: Item) -> bool:
        if len(self.items) + item.quantity <= self.capacity:
            self.items.append(item)
            return True
        return False
        
    def remove_item(self, item_type: ItemType, quantity: int = 1) -> Item | None:
        for item in self.items:
            if item.type == item_type:
                if item.quantity > quantity:
                    item.quantity -= quantity
                    return Item(item_type, item.name, quantity)
                elif item.quantity == quantity:
                    self.items.remove(item)
                    return item
        return None
        
    def get_item_count(self, item_type: ItemType) -> int:
        return sum(item.quantity for item in self.items if item.type == item_type)

    def is_accessible_from(self, x, y, tile_x, tile_y):
        """Check if object can be accessed from the given position"""
        dx = abs(x - tile_x)
        dy = abs(y - tile_y)
        return dx + dy == 1  # Adjacent tile
