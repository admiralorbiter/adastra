from enum import Enum

from world.objects import Bed
from world.items import ItemType
from world.objects import StorageContainer
from world.pathfinding import find_path
from utils.config_manager import ConfigManager

class Skill(Enum):
    ENGINEER = "Engineer"
    PILOT = "Pilot"
    SCIENTIST = "Scientist"

class CrewMember:
    def __init__(self, name: str, skill: Skill):
        config = ConfigManager.get_instance()
        
        self.name = name
        self.skill = skill
        self.ship = None  # Add ship reference
        
        # Add position tracking
        self.x = 0
        self.y = 0
        
        # Basic needs from configuration
        self.hunger = config.get('crew.needs.hunger.initial', 51)
        self.sleep = config.get('crew.needs.sleep.initial', 100)
        self.oxygen = config.get('crew.needs.oxygen.initial', 100)
        
        self.mood = 100    # 100 = happy, 0 = very upset
        self.work_efficiency = 1.0  # Multiplier for work speed
        
        # Add movement properties
        self.move_path = []
        self.move_speed = config.get('crew.movement.base_speed', 2.0)
        self.target_x = None
        self.target_y = None
        
        self.current_action = None  # Initialize current_action
        self.target_object = None   # Add this to track target object

    def update(self, dt):
        # Skip updates if currently sleeping
        if self.current_action == "sleeping":
            self.rest()
            # Clear any movement path if we somehow got one while sleeping
            self.move_path = []
            self.target_object = None
            return

        # Gradually decrease needs over time
        self.hunger = max(0, self.hunger - 0.1 * dt)  # Increased hunger rate
        self.sleep = max(0, self.sleep - 0.01 * dt)
        
        # Check if needs food and not already heading to food
        if self.hunger < 50 and not self.current_action == "getting_food":
            # Only look for food if not moving or doing other actions
            if not self.move_path and not self.target_object:
                nearest = self.ship.find_nearest_storage(int(self.x), int(self.y))
                if nearest:
                    storage, pos = nearest
                    # Create path to storage
                    start = (int(self.x), int(self.y))
                    path = find_path(self.ship.decks[0], start, pos)
                    if path:
                        self.target_object = storage
                        self.current_action = "getting_food"
                        self.set_path(path)

        
        # Handle movement and actions
        if self.move_path:
            # Get the next target position
            target = self.move_path[0]
            
            # Calculate movement distance this frame
            move_distance = self.move_speed * dt
            
            # Calculate direction to target
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= move_distance:
                # Reached the next point in path
                self.x, self.y = target
                self.move_path.pop(0)
                
                # If we've reached our destination and have a target object
                if not self.move_path and self.target_object:
                    if isinstance(self.target_object, Bed):
                        self.current_action = "sleeping"
                        self.rest()
                    elif isinstance(self.target_object, StorageContainer):
                        if self.current_action == "getting_food":
                            self.eat_from_storage(self.target_object)
                            self.current_action = None
                            self.target_object = None
            else:
                # Move towards target
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance

    def eat(self):
        self.hunger = min(100, self.hunger + 30)

    def rest(self):
        old_sleep = self.sleep
        self.sleep = min(100, self.sleep + 20)
        
        # Wake up if fully rested
        if old_sleep < 100 and self.sleep >= 100:
            self.current_action = None
            self.target_object = None

    def set_path(self, path):
        self.move_path = path[1:]  # Skip first position (current position) 

    def eat_from_storage(self, storage: StorageContainer):
        food = storage.remove_item(ItemType.FOOD)
        if food:
            self.hunger = min(100, self.hunger + 50)  # Increased food benefit
            return True
        return False