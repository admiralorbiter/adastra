import pygame

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
        self.cable_view_active = False

    def initialize(self, screen_width, screen_height):
        from models.build import BuildUI
        from world.camera import Camera
        from world.ship import Ship
        from game.ship_builder import create_basic_ship
        from world.cables import CableSystem
        from rendering.cable_renderer import CableRenderer
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.cable_system = CableSystem()
        self.ship = create_basic_ship(self.cable_system)
        self.cable_system.ship = self.ship
        self.build_ui = BuildUI(screen_width, self)
        self.camera = Camera(screen_width, screen_height)
        self.cable_renderer = CableRenderer()
        self.cable_view_active = False
        
        # Center camera on ship
        ship_width = self.ship.decks[0].width * 32  # TILE_SIZE
        ship_height = self.ship.decks[0].height * 32
        self.camera.center_on(ship_width, ship_height) 