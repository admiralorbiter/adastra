from world.objects import BaseObject
from typing import Optional, List
from models.enemies import Enemy

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
        self._x = 0
        self._y = 0
        self.enemies = []
        
    @property
    def x(self):
        return self._x
        
    @x.setter
    def x(self, value):
        self._x = value
        
    @property
    def y(self):
        return self._y
        
    @y.setter
    def y(self, value):
        self._y = value

    def set_position(self, x: int, y: int):
        """Explicitly set the weapon position"""
        self._x = x
        self._y = y
        print(f"Setting weapon position to ({x}, {y})")

    def update(self, dt):
        # Store coordinates for debugging
        print(f"\nWeapon position check - x: {self._x}, y: {self._y}")
        print(f"Number of enemies available: {len(self.enemies)}")
        
        # Check power state
        if hasattr(self, 'tile') and self.tile:
            self.powered = self.tile.has_power(self.power_required)
            print(f"Power check: {self.powered}")
        else:
            self.powered = False
            
        if not self.powered:
            return
            
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)

    def can_attack(self) -> bool:
        print("\nChecking can_attack:")
        if self.current_cooldown > 0:
            print("  Cooldown active")
            return False
            
        if not self.target:
            print("  No target")
            return False
            
        if not self.powered:
            print("  Not powered")
            return False
            
        if self.target.is_dead():
            print("  Target is dead")
            return False
            
        # Check if target is in range using tile coordinates
        dx = self.target.x - self._x
        dy = self.target.y - self._y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        in_range = distance <= self.range
        print(f"  Distance to target: {distance}, Range: {self.range}, In range: {in_range}")
        return in_range

    def fire(self):
        if self.target and self.can_attack():
            self.target.take_damage(self.damage)
            self.current_cooldown = self.attack_cooldown

    def find_target(self, enemies: List[Enemy]) -> Optional[Enemy]:
        closest_enemy = None
        closest_distance = float('inf')
        
        print(f"\nWeapon at ({self._x}, {self._y}) searching for targets")
        print(f"Number of enemies to check: {len(enemies)}")
        print(f"Weapon range: {self.range}")
        
        for enemy in enemies:
            if enemy.is_dead():
                print(f"Skipping dead enemy at ({enemy.x}, {enemy.y})")
                continue
            
            dx = enemy.x - self._x
            dy = enemy.y - self._y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            print(f"Checking enemy at ({enemy.x}, {enemy.y}):")
            print(f"  Distance: {distance}, Range: {self.range}")
            
            if distance <= self.range and distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
                print(f"  -> New closest target found at distance {distance}!")
        
        return closest_enemy

class LaserTurret(Weapon):
    def __init__(self):
        super().__init__("Laser Turret")
        self.damage = 15
        self.range = 4
        self.attack_cooldown = 0.5
        self.power_required = 3
        self.firing_animation_time = 0
        self.firing = False
    
    def update(self, dt):
        # Call parent update first to handle power check
        super().update(dt)
        
        if not self.powered:
            return
        
        print(f"\nLaserTurret at ({self._x}, {self._y}):")
        print(f"  Target: {self.target}")
        print(f"  Cooldown: {self.current_cooldown}")
        print(f"  Firing: {self.firing}")
        print(f"  Range: {self.range}")
        print(f"  Number of enemies: {len(self.enemies)}")
        
        # Try to find target if we don't have one
        if not self.target and self.powered:
            print("No target, searching...")
            self.target = self.find_target(self.enemies)
            if self.target:
                print(f"Found target at ({self.target.x}, {self.target.y})")
                self.fire()
        
        # Handle firing animation
        if self.firing_animation_time > 0:
            self.firing_animation_time -= dt
            if self.firing_animation_time <= 0:
                self.firing = False 