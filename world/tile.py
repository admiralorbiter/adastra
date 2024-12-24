class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.floor_type = "metal_floor"
        self.wall = False
        self.object = None
        self.module = None
        self.cable = None
        self.connected_modules = set()  # Track connected modules through cables

    def is_walkable(self):
        # Base tiles are walkable if they're not walls
        if self.wall:
            return False
        # Objects might block movement unless they're walkable
        if self.object and self.object.solid and not self.object.walkable:
            return False
        return True

    def has_power(self, required_power: float) -> bool:
        """Check if this tile has enough power for the required amount"""
        print(f"\nChecking power for tile ({self.x}, {self.y}):")
        # If there's no cable, there's no power
        if not self.cable:
            print("  No cable")
            return False
            
        # Check if the cable is powered and has enough capacity
        print(f"  Cable powered: {self.cable.powered}")
        if self.cable.powered and self.cable.network:
            print(f"  Network available power: {self.cable.network.available_power}")
            print(f"  Required power: {required_power}")
            return self.cable.network.available_power >= required_power
            
        return False

    def get_available_power(self) -> float:
        """Get the amount of power available at this tile"""
        if not self.cable or not self.cable.powered or not self.cable.network:
            return 0
        return self.cable.network.available_power
