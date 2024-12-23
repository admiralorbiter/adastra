import pygame

from game.ship_builder import create_basic_ship
from game.time_manager import TimeManager
from models.builders.build import BuildMode
from rendering.build_ui import BuildUI
from rendering.cable_renderer import CableRenderer
from utils.constants import GameConstants
from utils.config_manager import ConfigManager
from world.cables import CableSystem
from world.camera import Camera
from game.states.state_manager import StateManager
from game.states.game_states import GameState as GameStateEnum

class GameState:
    def __init__(self):
        self.selected_crew = None
        self.build_ui = None
        self.ship = None
        self.camera = None
        self.running = True
        self.screen = None
        self.clock = None
        self.cable_system = None
        self.cable_renderer = None
        self.time_manager = None
        
        # Add state manager
        self.state_manager = StateManager()
        self._setup_state_handlers()

    def _setup_state_handlers(self):
        # Register state handlers
        self.state_manager.register_state_handler(GameStateEnum.PLAYING, self._handle_playing)
        self.state_manager.register_state_handler(GameStateEnum.PAUSED, self._handle_paused)
        self.state_manager.register_state_handler(GameStateEnum.BUILDING, self._handle_building)
        
        # Register enter/exit handlers
        self.state_manager.register_state_enter_handler(GameStateEnum.PAUSED, self._enter_paused)
        self.state_manager.register_state_exit_handler(GameStateEnum.PAUSED, self._exit_paused)
        
    def _handle_playing(self, dt: float):
        """Handle playing state updates"""
        self.ship.update(dt)
        
    def _handle_paused(self, dt: float):
        """Handle paused state updates"""
        pass  # No updates while paused
        
    def _handle_building(self, dt: float):
        """Handle building state updates"""
        self.ship.update(dt)  # Still update ship for visual feedback
        
    def _enter_paused(self):
        """Called when entering paused state"""
        self.time_manager.paused = True
        
    def _exit_paused(self):
        """Called when exiting paused state"""
        self.time_manager.paused = False
        
    def update(self, dt: float):
        """Main update method"""
        self.state_manager.update(dt)

    def initialize(self, screen_width=None, screen_height=None):
        config = ConfigManager.get_instance()
        
        # Use provided dimensions or fall back to config
        screen_width = screen_width or config.get('game.window.width')
        screen_height = screen_height or config.get('game.window.height')
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(config.get('game.window.title', 'Ad Astra'))
        self.clock = pygame.time.Clock()
        self.cable_system = CableSystem()
        self.ship = create_basic_ship(self.cable_system)
        self.cable_system.ship = self.ship
        self.build_ui = BuildUI(screen_width, self)
        self.camera = Camera(screen_width, screen_height)
        self.cable_renderer = CableRenderer()
        self.time_manager = TimeManager()
        
        # Center camera on ship
        ship_width = self.ship.decks[0].width * GameConstants.get_instance().TILE_SIZE
        ship_height = self.ship.decks[0].height * GameConstants.get_instance().TILE_SIZE
        self.camera.center_on(ship_width, ship_height) 

    @property
    def show_cables(self):
        """Property to determine if cables should be shown"""
        return (self.state_manager.current_state == GameStateEnum.BUILDING and 
                self.build_ui and 
                self.build_ui.build_system.current_mode == BuildMode.CABLE) 