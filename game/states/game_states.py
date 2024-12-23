from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    BUILDING = auto()
    PAUSED = auto()
    CREW_MANAGEMENT = auto() 