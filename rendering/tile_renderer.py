import pygame
from .base_renderer import BaseRenderer

class TileRenderer(BaseRenderer):
    def draw_tiles(self, screen, deck, camera):
        """Draw all base tiles"""
        tile_size = self.get_scaled_size(camera)
        
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                screen_x, screen_y = self.get_screen_position(camera, x, y)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                # Draw the tile
                color = (50, 50, 50) if tile.wall else (200, 200, 200)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border

    def draw_build_highlights(self, screen, ship, camera, current_item):
        """Draw build mode highlights"""
        if not current_item or not ship.decks:
            return
            
        deck = ship.decks[0]
        tile_size = self.get_scaled_size(camera)
        
        for y in range(deck.height):
            for x in range(deck.width):
                if current_item.can_build(ship, x, y):
                    screen_x, screen_y = self.get_screen_position(camera, x, y)
                    s = pygame.Surface((tile_size, tile_size))
                    s.set_alpha(128)
                    s.fill((0, 255, 0))
                    screen.blit(s, (screen_x, screen_y)) 