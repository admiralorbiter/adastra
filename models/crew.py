from enum import Enum

class Skill(Enum):
    ENGINEER = "Engineer"
    PILOT = "Pilot"
    SCIENTIST = "Scientist"

class CrewMember:
    def __init__(self, name: str, skill: Skill):
        self.name = name
        self.skill = skill
        
        # Add position tracking
        self.x = 0
        self.y = 0
        
        # Basic needs (0-100 scale)
        self.hunger = 100  # 100 = full, 0 = starving
        self.sleep = 100   # 100 = well-rested, 0 = exhausted
        self.oxygen = 100  # 100 = normal, 0 = critical
        
        self.mood = 100    # 100 = happy, 0 = very upset
        self.work_efficiency = 1.0  # Multiplier for work speed
        
        # Add movement properties
        self.move_path = []
        self.move_speed = 2.0  # Tiles per second
        self.target_x = None
        self.target_y = None

    def update(self, dt):
        # Gradually decrease needs over time
        self.hunger = max(0, self.hunger - 0.01)
        self.sleep = max(0, self.sleep - 0.05)
        
        # Calculate mood based on needs
        self.mood = (self.hunger + self.sleep + self.oxygen) / 3
        
        # Update work efficiency based on mood
        if self.mood > 75:
            self.work_efficiency = 1.0
        elif self.mood > 50:
            self.work_efficiency = 0.8
        elif self.mood > 25:
            self.work_efficiency = 0.6
        else:
            self.work_efficiency = 0.4
        
        # Handle movement
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
            else:
                # Move towards target
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance

    def eat(self):
        self.hunger = min(100, self.hunger + 30)

    def rest(self):
        self.sleep = min(100, self.sleep + 20) 

    def set_path(self, path):
        self.move_path = path[1:]  # Skip first position (current position) 