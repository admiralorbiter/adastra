import pygame
from world import camera, ship
from world.pathfinding import find_path

TILE_SIZE = 32

class EventHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def handle_events(self):
        # Handle keyboard state for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.game_state.camera.move(0, 5)   # Move up (positive y)
        if keys[pygame.K_s]:
            self.game_state.camera.move(0, -5)  # Move down (negative y)
        if keys[pygame.K_a]:
            self.game_state.camera.move(5, 0)   # Move left (positive x)
        if keys[pygame.K_d]:
            self.game_state.camera.move(-5, 0)  # Move right (negative x)

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
            return  # Return early if UI handled the click
        
        # Convert screen coordinates to world coordinates once
        world_x, world_y = self.game_state.camera.screen_to_world(mouse_x, mouse_y)
        grid_x, grid_y = int(world_x // TILE_SIZE), int(world_y // TILE_SIZE)
        
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
            
            # Handle crew selection and movement
            clicked_on_crew = False
            for crew in self.game_state.ship.crew:
                if int(crew.x) == grid_x and int(crew.y) == grid_y:
                    self.game_state.selected_crew = crew
                    clicked_on_crew = True
                    break
            
            # Handle crew movement if we have a selected crew
            if self.game_state.selected_crew and not clicked_on_crew:
                if (grid_x < self.game_state.ship.decks[0].width and 
                    grid_y < self.game_state.ship.decks[0].height and 
                    self.game_state.ship.decks[0].tiles[grid_y][grid_x].is_walkable()):
                    start = (int(self.game_state.selected_crew.x), int(self.game_state.selected_crew.y))
                    goal = (grid_x, grid_y)
                    path = find_path(self.game_state.ship.decks[0], start, goal)
                    if path:
                        self.game_state.selected_crew.set_path(path)
                
                self.game_state.selected_crew = None

    def handle_mouse_motion(self, event):
        if self.game_state.cable_view_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x, world_y = self.game_state.camera.screen_to_world(mouse_x, mouse_y)
            # Convert world coordinates to grid coordinates
            grid_x = int(world_x / TILE_SIZE)
            grid_y = int(world_y / TILE_SIZE)
            self.game_state.cable_system.update_drag(grid_x, grid_y)

    def handle_mouse_up(self, event):
        if event.button == 1 and self.game_state.cable_view_active:
            self.game_state.cable_system.end_drag()
            self.game_state.cable_view_active = False