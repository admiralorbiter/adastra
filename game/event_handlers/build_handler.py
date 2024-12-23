import pygame
from .base_handler import BaseEventHandler

class BuildEventHandler(BaseEventHandler):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.dragging = False
        self.rect_select_start = None
        self.rect_select_end = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.dragging = True
                self.handle_left_click(event)
            elif event.button == 3:  # Right click
                self.handle_right_click(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                self.handle_left_release(event)
            elif event.button == 3:
                self.rect_select_start = None
                self.rect_select_end = None
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)

    def handle_left_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)
        current_item = self.game_state.build_ui.build_system.get_current_item()
        
        if current_item:
            if current_item.name == "Power Cable":
                self.game_state.cable_view_active = True
                self.game_state.cable_system.start_drag(grid_x, grid_y)
            elif 0 <= grid_x <= self.game_state.ship.decks[0].width and 0 <= grid_y <= self.game_state.ship.decks[0].height:
                current_item.build(self.game_state.ship, grid_x, grid_y)

    def handle_left_release(self, event):
        """Handle mouse left button release"""
        if self.game_state.cable_view_active:
            self.game_state.cable_system.end_drag()
            self.game_state.cable_view_active = False
        elif self.rect_select_start and self.rect_select_end:
            self.place_floor_rectangle()

    def handle_right_click(self, event):
        current_item = self.game_state.build_ui.build_system.get_current_item()
        if current_item and current_item.name == "Basic Floor":
            mouse_pos = pygame.mouse.get_pos()
            self.rect_select_start = self.game_state.camera.screen_to_grid(*mouse_pos)
        else:
            self.game_state.build_ui.clear_selection()

    def handle_mouse_motion(self, event):
        if self.game_state.cable_view_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)
            self.game_state.cable_system.update_drag(grid_x, grid_y)
        elif self.rect_select_start:
            mouse_pos = pygame.mouse.get_pos()
            self.rect_select_end = self.game_state.camera.screen_to_grid(*mouse_pos)

    def place_floor_rectangle(self):
        """Place floors in the selected rectangle"""
        if not self.rect_select_start or not self.rect_select_end:
            return
            
        start_x, start_y = self.rect_select_start
        end_x, end_y = self.rect_select_end
        
        # Ensure start is top-left and end is bottom-right
        min_x, max_x = min(start_x, end_x), max(start_x, end_x)
        min_y, max_y = min(start_y, end_y), max(start_y, end_y)
        
        current_item = self.game_state.build_ui.build_system.get_current_item()
        if current_item and current_item.name == "Basic Floor":
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    current_item.build(self.game_state.ship, x, y) 