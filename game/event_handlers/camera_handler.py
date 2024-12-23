import pygame
from .base_handler import BaseEventHandler

class CameraEventHandler(BaseEventHandler):
    def handle_keyboard_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.game_state.camera.move(0, 5)
        if keys[pygame.K_s]:
            self.game_state.camera.move(0, -5)
        if keys[pygame.K_a]:
            self.game_state.camera.move(5, 0)
        if keys[pygame.K_d]:
            self.game_state.camera.move(-5, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.game_state.camera.adjust_zoom(event.button == 4, mouse_x, mouse_y) 