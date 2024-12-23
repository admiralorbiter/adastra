class BaseModule:
    def __init__(self, name):
        self.name = name
        self.power_required = 0
        self.power_available = 0
        self.connected_cables = set()  # Store connected cable coordinates

    def update(self, dt):
        pass

    def is_powered(self):
        return self.power_available >= self.power_required

class LifeSupportModule(BaseModule):
    def __init__(self, name="Life Support Unit", oxygen_rate=1):
        super().__init__(name)
        self.oxygen_rate = oxygen_rate
        self.active = True
        self.power_required = 2  # Requires 2 power to operate

    @property
    def oxygen_production(self):
        # Only produce oxygen if powered
        return self.oxygen_rate if self.active and self.is_powered() else 0

class ReactorModule(BaseModule):
    def __init__(self, name="Basic Reactor", power_output=10):
        super().__init__(name)
        self.power_output = power_output
        self.power_available = power_output  # Reactors generate their own power

class EngineModule(BaseModule):
    def __init__(self, name="Basic Engine", thrust_power=5):
        super().__init__(name)
        self.thrust_power = thrust_power
        self.power_required = 3  # Requires 3 power to operate
        self.active = True

    @property
    def thrust_output(self):
        # Only produce thrust if powered
        return self.thrust_power if self.active and self.is_powered() else 0

class DockingDoorModule(BaseModule):
    def __init__(self, name="Docking Door"):
        super().__init__(name)
        self.power_required = 2  # Requires 2 power to operate
        self.active = True
        self.is_open = False
        self.direction = None  # 'horizontal' or 'vertical'
        self.primary_position = None  # (x, y) of primary tile
        self.secondary_position = None  # (x, y) of secondary tile

    def update(self, dt):
        # Update door state based on power
        if not self.is_powered():
            self.is_open = False

    @property
    def can_open(self):
        return self.active and self.is_powered()
