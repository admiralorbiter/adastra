import pygame
from world import camera, ship
from world.pathfinding import find_path

TILE_SIZE = 32

class EventHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

    def handle_mouse_down(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Handle UI clicks first
        if self.game_state.build_ui.handle_click((mouse_x, mouse_y)):
            return  # Return early if UI handled the click

        if event.button == 1:  # Left mouse button
            # Convert screen coordinates to world coordinates
            world_x, world_y = self.game_state.camera.screen_to_world(mouse_x, mouse_y)
            grid_x, grid_y = world_x // TILE_SIZE, world_y // TILE_SIZE
            
            # If in build mode, handle building
            current_item = self.game_state.build_ui.build_system.get_current_item()
            if current_item and grid_x < self.game_state.ship.decks[0].width and grid_y < self.game_state.ship.decks[0].height:
                current_item.build(self.game_state.ship, grid_x, grid_y)
            else:
                # Check if clicking on a crew member
                clicked_on_crew = False
                for crew in self.game_state.ship.crew:
                    if int(crew.x) == grid_x and int(crew.y) == grid_y:
                        self.game_state.selected_crew = crew
                        clicked_on_crew = True
                        break
                
                # If we have a selected crew and didn't click on another crew,
                # try to move the selected crew
                if self.game_state.selected_crew and not clicked_on_crew:
                    if (grid_x < self.game_state.ship.decks[0].width and 
                        grid_y < self.game_state.ship.decks[0].height and 
                        self.game_state.ship.decks[0].tiles[grid_y][grid_x].is_walkable()):
                        start = (int(self.game_state.selected_crew.x), int(self.game_state.selected_crew.y))
                        goal = (grid_x, grid_y)
                        path = find_path(self.game_state.ship.decks[0], start, goal)
                        if path:
                            self.game_state.selected_crew.set_path(path)
                    
                    # Deselect crew after setting path
                    self.game_state.selected_crew = None
        elif event.button == 3:  # Right mouse button
            self.game_state.camera.start_pan(mouse_x, mouse_y)

    def handle_mouse_up(self, event):
       if event.button == 3:  # Right mouse button
            self.game_state.camera.stop_pan()

    def handle_mouse_motion(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.game_state.camera.update_pan(mouse_x, mouse_y)