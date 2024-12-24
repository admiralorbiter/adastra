from world.items import Item, ItemType
from typing import Optional
from models.enemies import Enemy

class BaseObject:
    def __init__(self, name: str):
        self.name = name
        self.solid = False
        self.walkable = True
        self.x = 0
        self.y = 0

    def update(self, dt):
        """Base update method - override in subclasses if needed"""
        pass

class Weapon(BaseObject):
    def __init__(self, name: str):
        super().__init__(name)
        self.solid = True
        self.walkable = False
        self.damage = 0
        self.range = 0
        self.attack_cooldown = 1.0
        self.current_cooldown = 0
        self.powered = False
        self.power_required = 2
        self.target: Optional[Enemy] = None

    def update(self, dt):
        if not self.powered:
            return
            
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)
            
        if self.target and self.can_attack():
            self.fire()

    def can_attack(self) -> bool:
        if self.current_cooldown > 0:
            return False
            
        if not self.target:
            return False
            
        # Check if target is in range
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.range

    def fire(self):
        if self.target and self.can_attack():
            self.target.take_damage(self.damage)
            self.current_cooldown = self.attack_cooldown

    def find_target(self, enemies: list[Enemy]) -> Optional[Enemy]:
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= self.range and distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
                
        return closest_enemy

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
        # Convert to grid coordinates if needed
        grid_x = int(x)
        grid_y = int(y)
        grid_tile_x = int(tile_x)
        grid_tile_y = int(tile_y)
        dx = abs(grid_x - grid_tile_x)
        dy = abs(grid_y - grid_tile_y)
        return dx + dy == 1  # Adjacent tile

class Tank(BaseObject):
    def __init__(self, name="Storage Tank", capacity: int = 1000):
        super().__init__(name)
        self.solid = True
        self.walkable = False
        self.capacity = capacity
        self.resources = {
            ItemType.WATER: 0,
            ItemType.OXYGEN: 0
        }

    def add_resource(self, resource_type: ItemType, amount: float) -> float:
        """Add resource to tank, returns amount that couldn't be added"""
        if resource_type not in self.resources:
            return amount
            
        space_left = self.capacity - self.resources[resource_type]
        amount_to_add = min(amount, space_left)
        self.resources[resource_type] += amount_to_add
        return amount - amount_to_add

    def remove_resource(self, resource_type: ItemType, amount: float) -> float:
        """Remove resource from tank, returns amount actually removed"""
        if resource_type not in self.resources:
            return 0
            
        amount_to_remove = min(amount, self.resources[resource_type])
        self.resources[resource_type] -= amount_to_remove
        return amount_to_remove

    def get_fill_percentage(self, resource_type: ItemType) -> float:
        """Get fill percentage for a specific resource"""
        if resource_type not in self.resources:
            return 0
        return (self.resources[resource_type] / self.capacity) * 100

    def get_amount(self, resource_type: ItemType) -> float:
        """Get current amount of a specific resource"""
        return self.resources.get(resource_type, 0)
