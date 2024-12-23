import pygame
from .camera_handler import CameraEventHandler
from .build_handler import BuildEventHandler
from .crew_handler import CrewEventHandler

class EventHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.camera_handler = CameraEventHandler(game_state)
        self.build_handler = BuildEventHandler(game_state)
        self.crew_handler = CrewEventHandler(game_state)

    @property
    def rect_select_start(self):
        return self.build_handler.rect_select_start

    @property
    def rect_select_end(self):
        return self.build_handler.rect_select_end

    def handle_events(self):
        # Handle continuous camera movement
        self.camera_handler.handle_keyboard_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            else:
                # Handle UI clicks first
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_state.build_ui.handle_click(mouse_pos):
                    continue

                # Delegate to specialized handlers
                self.camera_handler.handle_event(event)
                self.build_handler.handle_event(event)
                self.crew_handler.handle_event(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.game_state.time_manager.toggle_pause()
        elif event.key == pygame.K_1:
            self.game_state.time_manager.set_time_scale(1.0)
        elif event.key == pygame.K_3:
            self.game_state.time_manager.set_time_scale(3.0)