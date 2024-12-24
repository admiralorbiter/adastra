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
        self.ship = None  # Reference to parent ship
        
    def set_ship(self, ship):
        """Set reference to parent ship"""
        print(f"Setting ship reference for {self.name}")
        print(f"Previous ship reference: {self.ship}")
        print(f"New ship object id: {id(ship)}")
        self.ship = ship
        print(f"Stored ship reference id: {id(self.ship)}")
        
    def set_position(self, x: int, y: int):
        """Explicitly set the weapon position"""
        self.x = x
        self.y = y
        print(f"Setting weapon position to ({x}, {y})")

    def update(self, dt):
        print(f"\n=== WEAPON BASE UPDATE ===")
        print(f"Weapon: {self.name}")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Has ship reference: {self.ship is not None}")
        if self.ship:
            print(f"Ship enemies count: {len(self.ship.enemies)}")
            for enemy in self.ship.enemies:
                print(f"  - Enemy {enemy.name} at ({enemy.x}, {enemy.y}) health: {enemy.health}")
        
        # Check power state
        if hasattr(self, 'tile') and self.tile:
            self.powered = self.tile.has_power(self.power_required)
            print(f"Power check: {self.powered} (requires {self.power_required})")
        else:
            self.powered = False
            print("No tile reference - unpowered")
            
        if not self.powered:
            print("Weapon unpowered - skipping update")
            return
            
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)
            print(f"Cooldown active: {self.current_cooldown:.2f}s remaining")

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
        print("\n=== FIRE ATTEMPT ===")
        if self.target and self.can_attack():
            print(f"Firing at {self.target.name}!")
            print(f"Target health before: {self.target.health}")
            self.target.take_damage(self.damage)
            print(f"Target health after: {self.target.health}")
            self.current_cooldown = self.attack_cooldown
            print(f"Weapon on cooldown: {self.attack_cooldown}s")
        else:
            print("Cannot fire - conditions not met")

    def find_target(self, enemies: List[Enemy]) -> Optional[Enemy]:
        print("\n=== TARGET SEARCH DEBUG ===")
        print(f"Weapon at ({self.x}, {self.y})")
        print(f"Range: {self.range}")
        
        if not self.ship or not self.ship.enemies:
            print("No ship reference or no enemies!")
            return None
            
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in self.ship.enemies:
            print(f"\nChecking enemy: {enemy.name}")
            print(f"Enemy position: ({enemy.x}, {enemy.y})")
            
            if enemy.is_dead():
                print("Enemy is dead, skipping")
                continue
                
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            print(f"Distance to enemy: {distance}")
            print(f"In range? {distance <= self.range}")
            
            if distance <= self.range and distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
                print("New closest target found!")
        
        if closest_enemy:
            print(f"Selected target: {closest_enemy.name} at ({closest_enemy.x}, {closest_enemy.y})")
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
    
    def update(self, dt):
        print("\n=== LASER TURRET UPDATE ===")
        print(f"Current state:")
        print(f"  Position: ({self.x}, {self.y})")
        print(f"  Powered: {self.powered}")
        print(f"  Current target: {self.target.name if self.target else 'None'}")
        print(f"  Range: {self.range}")
        print(f"  Cooldown: {self.current_cooldown:.2f}")
        
        if self.ship:
            print(f"\nShip status:")
            print(f"  Enemy count: {len(self.ship.enemies)}")
            for enemy in self.ship.enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                print(f"  - Enemy {enemy.name} at ({enemy.x}, {enemy.y})")
                print(f"    Distance: {distance:.1f}, In range: {distance <= self.range}")
        else:
            print("No ship reference!")
        
        # Call parent update
        super().update(dt)
        
        if not self.powered:
            print("Turret unpowered - skipping targeting")
            return
            
        # Reset target if it's dead or null
        if self.target and self.target.is_dead():
            print(f"Current target {self.target.name} is dead - resetting target")
            self.target = None
            
        if not self.target and self.powered and self.ship:
            print("\nSearching for new target...")
            self.target = self.find_target(self.ship.enemies)
            if self.target:
                print(f"New target acquired: {self.target.name}")
                print(f"Attempting to fire...")
                self.fire()
            else:
                print("No valid target found")

    def fire(self):
        print("\n=== FIRE ATTEMPT ===")
        if self.target and self.can_attack():
            print(f"Firing at {self.target.name}!")
            print(f"Target health before: {self.target.health}")
            self.target.take_damage(self.damage)
            print(f"Target health after: {self.target.health}")
            self.current_cooldown = self.attack_cooldown
            print(f"Weapon on cooldown: {self.attack_cooldown}s")
        else:
            print("Cannot fire - conditions not met")