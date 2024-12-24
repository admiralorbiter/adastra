import pygame

from world import camera
from .base_renderer import BaseRenderer
from world.objects import Bed, StorageContainer, Tank
from world.weapons import LaserTurret
from world.items import ItemType

class ObjectRenderer(BaseRenderer):
    def draw_objects(self, screen, deck, camera):
        """Draw all objects"""
        tile_size = self.get_scaled_size(camera)
        
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                if not tile.object:
                    continue
                    
                screen_x, screen_y = self.get_screen_position(camera, x, y)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                self._draw_object(screen, tile.object, rect)

    def _draw_object(self, screen, obj, rect):
        """Draw a specific object"""
        if isinstance(obj, LaserTurret):
            # Draw range indicator (semi-transparent circle)
            range_radius = obj.range * rect.width
            range_surface = pygame.Surface((range_radius * 2, range_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 0, 0, 30), 
                             (range_radius, range_radius), range_radius)
            screen.blit(range_surface, 
                       (rect.centerx - range_radius, rect.centery - range_radius))

            # Draw turret base
            image = self.asset_loader.get_image('laser_turret')
            if image:
                scaled_image = pygame.transform.scale(image, (rect.width, rect.height))
                screen.blit(scaled_image, rect)
            else:
                # Fallback if image not found
                pygame.draw.rect(screen, (150, 0, 0), rect)  # Red base
                # Draw "X" for turret
                pygame.draw.line(screen, (255, 0, 0), rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, (255, 0, 0), rect.bottomleft, rect.topright, 2)
            
            # Draw laser beam if firing
            if obj.target and obj.can_attack() and obj.powered:
                start_pos = (rect.centerx, rect.centery)
                target_screen_x = int(obj.target.x * self.game_constants.TILE_SIZE * camera.zoom)
                target_screen_y = int(obj.target.y * self.game_constants.TILE_SIZE * camera.zoom)
                end_pos = camera.world_to_screen(target_screen_x, target_screen_y)
                
                # Draw laser beam
                pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)
                
                # Draw impact effect
                pygame.draw.circle(screen, (255, 100, 100), end_pos, 5)
            
            # Draw power indicator
            if obj.powered:
                indicator_size = 6
                pygame.draw.circle(screen, (0, 255, 0), 
                                 (rect.right - indicator_size, rect.top + indicator_size), 
                                 indicator_size)
            else:
                indicator_size = 6
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (rect.right - indicator_size, rect.top + indicator_size), 
                                 indicator_size)
            
            # Add debug info
            font = pygame.font.Font(None, 24)
            debug_info = [
                f"Powered: {obj.powered}",
                f"Target: {obj.target is not None}",
                f"Can Attack: {obj.can_attack() if obj.target else False}",
                f"Range: {obj.range}"
            ]
            
            y_offset = 0
            for text in debug_info:
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (rect.x, rect.y + y_offset))
                y_offset += 20
        
        elif isinstance(obj, Bed):
            image = self.asset_loader.get_image('bed')
            if image:
                scaled_image = pygame.transform.scale(image, (rect.width, rect.height))
                screen.blit(scaled_image, rect)
            else:
                pygame.draw.rect(screen, (139, 69, 19), rect)  # Brown fallback
                
        elif isinstance(obj, StorageContainer):
            image = self.asset_loader.get_image('container')
            if image:
                scaled_image = pygame.transform.scale(image, (rect.width, rect.height))
                screen.blit(scaled_image, rect)
            else:
                pygame.draw.rect(screen, (255, 255, 0), rect)  # Yellow fallback
                
        elif isinstance(obj, Tank):
            if obj.get_amount(ItemType.OXYGEN) > 0:
                color = (100, 100, 255)  # Blue for oxygen
            elif obj.get_amount(ItemType.WATER) > 0:
                color = (0, 191, 255)  # Light blue for water
            else:
                color = (150, 150, 150)  # Gray for empty tank
            pygame.draw.rect(screen, color, rect)
            
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border 