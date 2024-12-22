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
    def __init__(self, name="Life Support Unit", oxygen_rate=0.5):
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
