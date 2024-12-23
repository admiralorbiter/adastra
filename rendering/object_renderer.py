import pygame
from .base_renderer import BaseRenderer
from world.objects import Bed, StorageContainer, Tank
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
        if isinstance(obj, Bed):
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