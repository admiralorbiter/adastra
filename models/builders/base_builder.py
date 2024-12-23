from abc import ABC, abstractmethod

class BaseBuilder(ABC):
    def __init__(self, name: str, description: str, icon_color: tuple[int, int, int], cost: int = 10):
        self.name = name
        self.description = description
        self.icon_color = icon_color
        self.cost = cost

    @abstractmethod
    def can_build(self, ship, x: int, y: int) -> bool:
        """Check if item can be built at the specified location"""
        pass

    @abstractmethod
    def build(self, ship, x: int, y: int) -> bool:
        """Actually perform the building action"""
        pass 