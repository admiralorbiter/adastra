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

    def initialize(self, screen_width, screen_height):
        from models.build import BuildUI
        from world.camera import Camera
        from world.ship import Ship
        from game.ship_builder import create_basic_ship
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.ship = create_basic_ship()
        self.build_ui = BuildUI(screen_width)
        self.camera = Camera(screen_width, screen_height)
        
        # Center camera on ship
        ship_width = self.ship.decks[0].width * 32  # TILE_SIZE
        ship_height = self.ship.decks[0].height * 32
        self.camera.center_on(ship_width, ship_height) 