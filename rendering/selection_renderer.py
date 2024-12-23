import pygame
from .base_renderer import BaseRenderer
from world.objects import Bed

class SelectionRenderer(BaseRenderer):
    def draw_selection(self, screen, deck, camera, rect_select_start=None, rect_select_end=None):
        """Draw rectangle selection preview"""
        if not rect_select_start or not rect_select_end:
            return
            
        start_x, start_y = rect_select_start
        end_x, end_y = rect_select_end
        min_x, max_x = min(start_x, end_x), max(start_x, end_x)
        min_y, max_y = min(start_y, end_y), max(start_y, end_y)
        
        tile_size = self.get_scaled_size(camera)
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                screen_x, screen_y = camera.grid_to_screen(x, y)
                preview = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                preview.fill((0, 255, 0, 64))
                screen.blit(preview, (screen_x, screen_y))

    def draw_bed_highlights(self, screen, deck, camera, selected_crew):
        """Draw bed highlights when crew is selected"""
        if not selected_crew:
            return
            
        tile_size = self.get_scaled_size(camera)
        
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                if tile and tile.object and isinstance(tile.object, Bed):
                    screen_x, screen_y = self.get_screen_position(camera, x, y)
                    pygame.draw.rect(screen, (0, 255, 255), 
                                   (screen_x, screen_y, tile_size, tile_size), 2) 