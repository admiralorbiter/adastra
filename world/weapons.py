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

    def update(self, dt):
        # Store previous power state
        was_powered = self.powered
        
        # Check if connected to power
        if hasattr(self, 'tile') and self.tile:
            self.powered = self.tile.has_power(self.power_required)
            print(f"Power check - Has tile: True, Has power: {self.powered}")
        else:
            self.powered = False
            print("Power check - Has tile: False")
            
        # If we just got power, clear target to force retargeting
        if not was_powered and self.powered:
            print("Just got power - clearing target")
            self.target = None
            
        if not self.powered:
            print("Not powered - skipping update")
            return
            
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)
            print(f"Cooldown active: {self.current_cooldown}")
            
        if self.target and self.can_attack():
            print("Conditions met - firing!")
            self.fire()

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
        dx = self.target.x - self.x
        dy = self.target.y - self.y
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
        
        print(f"\nWeapon at ({self.x}, {self.y}) searching for targets")
        print(f"Weapon range: {self.range}")
        
        for enemy in enemies:
            if enemy.is_dead():
                print(f"Enemy at ({enemy.x}, {enemy.y}) is dead, skipping")
                continue
            
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            print(f"Checking enemy at ({enemy.x}, {enemy.y}):")
            print(f"  dx: {dx}, dy: {dy}")
            print(f"  distance: {distance}")
            print(f"  in range? {distance <= self.range}")
            
            if distance <= self.range and distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
                print(f"  -> New closest target at distance {distance}")
        
        if closest_enemy:
            print(f"Found target at ({closest_enemy.x}, {closest_enemy.y})")
        else:
            print("No valid target found")
        
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
    
    def fire(self):
        if self.target and self.can_attack():
            print(f"LaserTurret firing at target! Target health before: {self.target.health}")
            self.target.take_damage(self.damage)
            print(f"Target health after: {self.target.health}")
            self.current_cooldown = self.attack_cooldown
            self.firing = True
            self.firing_animation_time = 0.1
    
    def update(self, dt):
        super().update(dt)
        print(f"LaserTurret update - Firing: {self.firing}, Animation time: {self.firing_animation_time}")
        if self.firing_animation_time > 0:
            self.firing_animation_time -= dt
            if self.firing_animation_time <= 0:
                self.firing = False 