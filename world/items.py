from dataclasses import dataclass
from enum import Enum, auto

class ItemType(Enum):
    FOOD = auto()
    # Add more types as needed

@dataclass
class Item:
    type: ItemType
    name: str
    quantity: int = 1
    
class FoodItem(Item):
    def __init__(self, quantity=1):
        super().__init__(ItemType.FOOD, "Food Ration", quantity) 