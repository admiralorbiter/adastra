class Ship:
    def __init__(self, name="Unnamed Ship"):
        self.name = name
        self.decks = []
        self.global_oxygen = 100.0
        self.global_power = 0
        self.max_power = 0
        self.crew = []

    def add_deck(self, deck):
        self.decks.append(deck)

    def update(self, dt):
        # Update all decks and recalculate resources
        for deck in self.decks:
            deck.update(dt)
        
        # Update crew members with dt parameter
        for crew_member in self.crew:
            crew_member.update(dt)
            
        self.calculate_resources()

    def calculate_resources(self):
        total_power = 0
        life_support_oxygen = 0

        for deck in self.decks:
            for room in deck.rooms:
                for tile in room.tiles:
                    if tile.module:
                        mod = tile.module
                        # Check module type
                        if hasattr(mod, 'power_output'):
                            total_power += mod.power_output
                        if hasattr(mod, 'oxygen_production'):
                            life_support_oxygen += mod.oxygen_production

        self.max_power = total_power
        self.global_oxygen += life_support_oxygen
        if self.global_oxygen > 100.0:
            self.global_oxygen = 100.0

    def add_crew_member(self, crew_member):
        self.crew.append(crew_member)
