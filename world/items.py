from dataclasses import dataclass
from enum import Enum, auto

class ItemType(Enum):
    FOOD = auto()
    METAL = auto()
    WATER = auto()
    OXYGEN = auto()
    # Add more types as needed

@dataclass
class Item:
    type: ItemType
    name: str
    quantity: int = 1
    
class FoodItem(Item):
    def __init__(self, quantity=1):
        super().__init__(ItemType.FOOD, "Food Ration", quantity) 

class MetalItem(Item):
    def __init__(self, quantity=1):
        super().__init__(ItemType.METAL, "Metal", quantity)

class WaterItem(Item):
    def __init__(self, quantity=1):
        super().__init__(ItemType.WATER, "Water", quantity)

class OxygenItem(Item):
    def __init__(self, quantity=1):
        super().__init__(ItemType.OXYGEN, "Oxygen", quantity)