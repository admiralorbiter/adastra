import pygame
from world import camera, ship
from world.pathfinding import find_path
from world.objects import Bed
from utils.constants import GameConstants

class EventHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def handle_events(self):
        # Handle keyboard state for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.game_state.camera.move(0, 5)
        if keys[pygame.K_s]:
            self.game_state.camera.move(0, -5)
        if keys[pygame.K_a]:
            self.game_state.camera.move(5, 0)
        if keys[pygame.K_d]:
            self.game_state.camera.move(-5, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):  # Mouse wheel up (4) or down (5)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.game_state.camera.adjust_zoom(event.button == 4, mouse_x, mouse_y)
                else:
                    self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.game_state.time_manager.toggle_pause()
        elif event.key == pygame.K_1:
            self.game_state.time_manager.set_time_scale(1.0)
        elif event.key == pygame.K_3:
            self.game_state.time_manager.set_time_scale(3.0)

    def handle_mouse_down(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Handle UI clicks first
        if self.game_state.build_ui.handle_click((mouse_x, mouse_y)):
            return
        
        # Convert screen coordinates to grid coordinates using camera
        grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)
        
        if event.button == 1:  # Left mouse button
            current_item = self.game_state.build_ui.build_system.get_current_item()
            
            # Special handling for cable mode
            if current_item and current_item.name == "Power Cable":
                self.game_state.cable_view_active = True
                self.game_state.cable_system.start_drag(grid_x, grid_y)
                return True
            
            # Handle building if we have an item
            elif current_item:
                # Allow building within bounds or one tile beyond
                if 0 <= grid_x <= self.game_state.ship.decks[0].width and 0 <= grid_y <= self.game_state.ship.decks[0].height:
                    current_item.build(self.game_state.ship, grid_x, grid_y)
                    return True
            
            # Handle crew selection
            clicked_on_crew = False
            for crew in self.game_state.ship.crew:
                if int(crew.x) == grid_x and int(crew.y) == grid_y:
                    self.game_state.selected_crew = crew
                    clicked_on_crew = True
                    break
            
            # Handle crew movement or bed interaction if we have a selected crew
            if self.game_state.selected_crew and not clicked_on_crew:
                deck = self.game_state.ship.decks[0]
                if (grid_x < deck.width and grid_y < deck.height):
                    tile = deck.tiles[grid_y][grid_x]
                    
                    # Check if clicked on a bed
                    if tile.object and isinstance(tile.object, Bed):
                        start = (int(self.game_state.selected_crew.x), int(self.game_state.selected_crew.y))
                        goal = (grid_x, grid_y)
                        path = find_path(deck, start, goal)
                        if path:
                            self.game_state.selected_crew.target_object = tile.object
                            self.game_state.selected_crew.set_path(path)
                    # Regular movement
                    elif tile.is_walkable():
                        start = (int(self.game_state.selected_crew.x), int(self.game_state.selected_crew.y))
                        goal = (grid_x, grid_y)
                        path = find_path(deck, start, goal)
                        if path:
                            self.game_state.selected_crew.target_object = None
                            self.game_state.selected_crew.set_path(path)

    def handle_mouse_motion(self, event):
        if self.game_state.cable_view_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)
            self.game_state.cable_system.update_drag(grid_x, grid_y)

    def handle_mouse_up(self, event):
        if event.button == 1 and self.game_state.cable_view_active:
            self.game_state.cable_system.end_drag()
            self.game_state.cable_view_active = False

    def check_crew_click(self, grid_x, grid_y):
        if not self.game_state.ship.crew:
            return None
            
        for crew in self.game_state.ship.crew:
            if int(crew.x) == grid_x and int(crew.y) == grid_y:
                return crew
        return None

    def check_object_click(self, grid_x, grid_y):
        if not self.game_state.ship.decks:
            return None
            
        deck = self.game_state.ship.decks[0]
        if 0 <= grid_x < deck.width and 0 <= grid_y < deck.height:
            tile = deck.tiles[grid_y][grid_x]
            return tile.object if tile and hasattr(tile, 'object') else None
        return None

    def handle_click(self, mouse_pos):
        # Convert screen coordinates to world coordinates
        world_x, world_y = self.game_state.camera.screen_to_world(*mouse_pos)
        grid_x = int(world_x / 32)  # Assuming TILE_SIZE = 32
        grid_y = int(world_y / 32)
        
        # First, check if we clicked on a crew member
        for crew in self.game_state.ship.crew:
            crew_grid_x = int(crew.x)
            crew_grid_y = int(crew.y)
            if crew_grid_x == grid_x and crew_grid_y == grid_y:
                self.game_state.selected_crew = crew
                return
        
        # If we have a selected crew member, check if we clicked on a bed
        if self.game_state.selected_crew:
            deck = self.game_state.ship.decks[0]
            if 0 <= grid_x < deck.width and 0 <= grid_y < deck.height:
                tile = deck.tiles[grid_y][grid_x]
                if tile.object and isinstance(tile.object, Bed):
                    # Create a simple path (direct path for now)
                    crew = self.game_state.selected_crew
                    path = [(crew.x, crew.y), (grid_x, grid_y)]
                    crew.target_object = tile.object
                    crew.set_path(path)