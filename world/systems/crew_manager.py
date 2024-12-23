class CrewManager:
    def __init__(self):
        self.crew = []

    def add_crew_member(self, crew_member, ship):
        """Add a new crew member"""
        crew_member.ship = ship
        self.crew.append(crew_member)

    def remove_crew_member(self, crew_member):
        """Remove a crew member"""
        if crew_member in self.crew:
            self.crew.remove(crew_member)

    def update(self, dt):
        """Update all crew members"""
        for crew_member in self.crew:
            crew_member.update(dt)

    def get_crew_count(self) -> int:
        """Get total number of crew members"""
        return len(self.crew) 