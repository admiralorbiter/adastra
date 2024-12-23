from world.items import ItemType
from world.modules import ReactorModule

class ResourceManager:
    def __init__(self):
        self.global_oxygen = 100.0
        self.global_power = 0
        self.max_power = 0
        self.oxygen_capacity = 100.0
        self.oxygen_consumption_per_crew = 1
        self.oxygen_tanks = []
        self.water_tanks = []

    def update(self, dt, ship):
        """Update all resources"""
        self._update_power(ship)
        self._update_oxygen(dt, ship)

    def _update_power(self, ship):
        """Calculate and update power distribution"""
        total_power = 0
        for deck in ship.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module and hasattr(tile.module, 'power_output'):
                        total_power += tile.module.power_output
        self.max_power = total_power

    def _update_oxygen(self, dt, ship):
        """Calculate and update oxygen levels"""
        life_support_oxygen = 0
        for deck in ship.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module and hasattr(tile.module, 'oxygen_production'):
                        life_support_oxygen += tile.module.oxygen_production * dt

        total_oxygen_production = life_support_oxygen
        total_oxygen_consumption = len(ship.crew) * self.oxygen_consumption_per_crew * dt
        oxygen_change = total_oxygen_production - total_oxygen_consumption

        # Update oxygen levels
        self.global_oxygen = max(0.0, min(self.oxygen_capacity, self.global_oxygen + oxygen_change))
        self._handle_oxygen_storage(oxygen_change, ship)

    def _handle_oxygen_storage(self, oxygen_change, ship):
        """Handle oxygen storage in tanks"""
        if oxygen_change > 0:
            self._store_excess_oxygen(oxygen_change, ship)
        else:
            self._withdraw_needed_oxygen(-oxygen_change, ship)

    def _store_excess_oxygen(self, amount, ship):
        """Store excess oxygen in tanks"""
        remaining_oxygen = amount
        for tank in self.oxygen_tanks:
            remaining_oxygen = tank.add_resource(ItemType.OXYGEN, remaining_oxygen)
            if remaining_oxygen <= 0:
                break

    def _withdraw_needed_oxygen(self, amount, ship):
        """Withdraw needed oxygen from tanks"""
        needed_oxygen = amount
        for tank in self.oxygen_tanks:
            needed_oxygen -= tank.remove_resource(ItemType.OXYGEN, needed_oxygen)
            if needed_oxygen <= 0:
                break

    def add_tank(self, tank):
        """Add a new resource tank"""
        if tank.resource_type == ItemType.OXYGEN:
            self.oxygen_tanks.append(tank)
        elif tank.resource_type == ItemType.WATER:
            self.water_tanks.append(tank)

    def get_total_oxygen(self) -> float:
        return sum(tank.current_amount for tank in self.oxygen_tanks)

    def get_total_oxygen_capacity(self) -> float:
        return sum(tank.capacity for tank in self.oxygen_tanks)

    def get_total_water(self) -> float:
        return sum(tank.current_amount for tank in self.water_tanks) 