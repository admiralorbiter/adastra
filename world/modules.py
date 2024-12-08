class BaseModule:
    def __init__(self, name):
        self.name = name

    def update(self, dt):
        pass

class LifeSupportModule(BaseModule):
    def __init__(self, name="Life Support Unit", oxygen_rate=0.5):
        super().__init__(name)
        self.oxygen_rate = oxygen_rate

    @property
    def oxygen_production(self):
        return self.oxygen_rate

class ReactorModule(BaseModule):
    def __init__(self, name="Basic Reactor", power_output=10):
        super().__init__(name)
        self.power_output = power_output
