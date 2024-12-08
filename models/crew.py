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

    def update(self):
        # Gradually decrease needs over time
        self.hunger = max(0, self.hunger - 0.1)
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

    def eat(self):
        self.hunger = min(100, self.hunger + 30)

    def rest(self):
        self.sleep = min(100, self.sleep + 20) 