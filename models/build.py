from enum import Enum, auto
from models.builders.base_builder import BaseBuilder
from models.builders.floor_builder import FloorBuilder
from models.builders.wall_builder import WallBuilder
from models.builders.module_builder import ModuleBuilder
from models.builders.cable_builder import CableBuilder
from models.builders.object_builder import ObjectBuilder
from world.modules import LifeSupportModule, ReactorModule, EngineModule
from world.objects import Bed, StorageContainer, Tank

class BuildMode(Enum):
    NONE = auto()
    FLOOR = auto()
    WALL = auto()
    CABLE = auto()
    OBJECT = auto()
    MODULE = auto()

class BuildCategory:
    def __init__(self, mode: BuildMode, items: list[BaseBuilder]):
        self.mode = mode
        self.items = items
        self.selected_item: BaseBuilder | None = None

class BuildSystem:
    def __init__(self):
        self.current_mode = BuildMode.NONE
        self.categories = {
            BuildMode.FLOOR: BuildCategory(BuildMode.FLOOR, [
                FloorBuilder("Basic Floor", "A simple metal floor", (200, 200, 200)),
            ]),
            BuildMode.WALL: BuildCategory(BuildMode.WALL, [
                WallBuilder("Basic Wall", "Standard wall panel", (100, 100, 100)),
            ]),
            BuildMode.CABLE: BuildCategory(BuildMode.CABLE, [
                CableBuilder("Power Cable", "Basic power cable", (255, 140, 0)),
            ]),
            BuildMode.OBJECT: BuildCategory(BuildMode.OBJECT, [
                ObjectBuilder("Bed", "A place for crew to rest", (139, 69, 19), Bed),
                ObjectBuilder("Storage Container", "Store items and resources", (160, 82, 45), StorageContainer),
                ObjectBuilder("Storage Tank", "Store liquids and gases", (0, 191, 255), Tank)
            ]),
            BuildMode.MODULE: BuildCategory(BuildMode.MODULE, [
                ModuleBuilder("Life Support", "Generates oxygen for the ship", (100, 100, 255), LifeSupportModule),
                ModuleBuilder("Reactor", "Generates power for the ship", (255, 140, 0), ReactorModule),
                ModuleBuilder("Engine", "Provides thrust for ship movement", (50, 255, 50), EngineModule)
            ])
        }
        self.active_category: BuildCategory | None = None

    def set_mode(self, mode: BuildMode) -> None:
        if self.current_mode == mode:
            self.current_mode = BuildMode.NONE
            self.active_category = None
        else:
            self.current_mode = mode
            self.active_category = self.categories.get(mode)
            if self.active_category:
                self.active_category.selected_item = self.active_category.items[0]

    def get_current_item(self) -> BaseBuilder | None:
        """Get the currently selected build item"""
        if self.active_category:
            return self.active_category.selected_item
        return None

    def clear_selection(self):
        """Clear the current build mode and selection"""
        self.current_mode = BuildMode.NONE
        self.active_category = None
        # Deactivate all category selections
        for category in self.categories.values():
            category.selected_item = None 