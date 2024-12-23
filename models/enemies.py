from enum import Enum
from typing import Optional

class EnemyType(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"

class Enemy:
    def __init__(self, name: str, enemy_type: EnemyType):
        # Basic properties
        self.name = name
        self.enemy_type = enemy_type
        self.ship = None  # Reference to ship they're attacking
        
        # Position tracking
        self.x = 0
        self.y = 0
        
        # Combat stats
        self.health = 100
        self.max_health = 100
        self.damage = 10
        self.attack_range = 1 if enemy_type == EnemyType.MELEE else 3
        self.attack_cooldown = 2.0  # Seconds between attacks
        self.current_cooldown = 0
        
        # Movement properties
        self.move_path = []
        self.move_speed = 1.5  # Slightly slower than crew
        self.target_x = None
        self.target_y = None
        
        # AI properties
        self.current_action = None
        self.target_object = None
        self.target_crew = None

    def update(self, dt):
        # Update attack cooldown
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)
            
        # Handle movement similar to crew
        if self.move_path:
            target = self.move_path[0]
            move_distance = self.move_speed * dt
            
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= move_distance:
                self.x, self.y = target
                self.move_path.pop(0)
            else:
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance

    def set_path(self, path):
        self.move_path = path[1:]  # Skip first position (current position)

    def attack(self, target) -> bool:
        """Attempt to attack a target"""
        if self.current_cooldown > 0:
            return False
            
        # Check if target is in range
        dx = target.x - self.x
        dy = target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance <= self.attack_range:
            self.current_cooldown = self.attack_cooldown
            return True
        return False

    def take_damage(self, amount: float):
        """Take damage and return True if enemy dies"""
        self.health = max(0, self.health - amount)
        return self.health <= 0 

class MeleeEnemy(Enemy):
    def __init__(self, name: str):
        super().__init__(name, EnemyType.MELEE)
        self.damage = 15  # Higher damage but must be close
        self.move_speed = 1.8  # Faster movement to close distance
        self.health = 120  # More health since they need to get close

class RangedEnemy(Enemy):
    def __init__(self, name: str):
        super().__init__(name, EnemyType.RANGED)
        self.damage = 8  # Lower damage but can attack from range
        self.move_speed = 1.2  # Slower movement
        self.health = 80  # Less health since they can attack from range 