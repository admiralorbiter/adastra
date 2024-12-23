import pygame
from .base_renderer import BaseRenderer

class CrewRenderer(BaseRenderer):
    def draw_crew(self, screen, crew_list, camera, selected_crew=None):
        """Draw all crew members"""
        for crew in crew_list:
            screen_x, screen_y = camera.world_to_screen(
                crew.x * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2,
                crew.y * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2
            )
            
            # Draw crew member
            radius = int((self.game_constants.TILE_SIZE//3) * camera.zoom)
            pygame.draw.circle(screen, (0, 255, 0), (screen_x, screen_y), radius)
            
            # Draw selection highlight if selected
            if crew == selected_crew:
                highlight_radius = int((self.game_constants.TILE_SIZE//2) * camera.zoom)
                pygame.draw.circle(screen, (255, 255, 255), 
                                (screen_x, screen_y), 
                                highlight_radius,
                                max(1, int(2 * camera.zoom)))

    def draw_path(self, screen, crew, camera):
        """Draw movement path for selected crew"""
        if not crew or not crew.move_path:
            return
            
        path_points = []
        start_x, start_y = camera.world_to_screen(
            crew.x * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2,
            crew.y * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2
        )
        path_points.append((start_x, start_y))
        
        for x, y in crew.move_path:
            screen_x, screen_y = camera.world_to_screen(
                x * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2,
                y * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2
            )
            path_points.append((screen_x, screen_y))
            
        pygame.draw.lines(screen, (255, 255, 0), False, path_points, 2) 