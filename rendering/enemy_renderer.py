import pygame
from .base_renderer import BaseRenderer
from models.enemies import Enemy, EnemyType

class EnemyRenderer(BaseRenderer):
    def draw_enemies(self, screen, enemy_list, camera, selected_enemy=None):
        """Draw all enemies"""
        for enemy in enemy_list:
            screen_x, screen_y = camera.world_to_screen(
                enemy.x * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2,
                enemy.y * self.game_constants.TILE_SIZE + self.game_constants.TILE_SIZE // 2
            )
            
            # Draw enemy (red circle)
            radius = int((self.game_constants.TILE_SIZE//3) * camera.zoom)
            pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), radius)
            
            # Draw health bar
            self._draw_health_bar(screen, enemy, screen_x, screen_y, camera.zoom)
            
            # Draw enemy type indicator
            if enemy.enemy_type == EnemyType.RANGED:
                # Draw a small ring around ranged enemies
                outer_radius = radius + max(2, int(2 * camera.zoom))
                pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 
                                outer_radius, max(1, int(camera.zoom)))
            
            # Draw selection highlight if selected
            if enemy == selected_enemy:
                highlight_radius = int((self.game_constants.TILE_SIZE//2) * camera.zoom)
                pygame.draw.circle(screen, (255, 255, 255), 
                                (screen_x, screen_y), 
                                highlight_radius,
                                max(1, int(2 * camera.zoom)))

    def _draw_health_bar(self, screen, enemy, x, y, zoom):
        """Draw health bar above enemy"""
        bar_width = int(self.game_constants.TILE_SIZE * 0.8 * zoom)
        bar_height = max(2, int(4 * zoom))
        
        # Background (red)
        bg_rect = pygame.Rect(
            x - bar_width//2,
            y - int(self.game_constants.TILE_SIZE//2 * zoom) - bar_height - 2,
            bar_width,
            bar_height
        )
        pygame.draw.rect(screen, (200, 0, 0), bg_rect)
        
        # Health (green)
        health_width = int(bar_width * (enemy.health / enemy.max_health))
        health_rect = pygame.Rect(
            x - bar_width//2,
            y - int(self.game_constants.TILE_SIZE//2 * zoom) - bar_height - 2,
            health_width,
            bar_height
        )
        pygame.draw.rect(screen, (0, 200, 0), health_rect) 