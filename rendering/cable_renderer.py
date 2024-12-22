import pygame

TILE_SIZE = 32

class CableRenderer:
    def __init__(self):
        self.cable_color = (255, 140, 0)  # Orange for cables
        self.preview_color = (255, 140, 0, 128)  # Semi-transparent orange
        
    def draw_cables(self, screen, ship, camera, cable_system):
        if not ship.decks:
            return
            
        deck = ship.decks[0]
        
        # Draw existing cables
        for (x, y), cable in cable_system.cables.items():
            if 0 <= x < deck.width and 0 <= y < deck.height:
                screen_x, screen_y = camera.world_to_screen(x * TILE_SIZE, y * TILE_SIZE)
                rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, self.cable_color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        
        # Draw preview cables
        for x, y in cable_system.preview_cables:
            if 0 <= x < deck.width and 0 <= y < deck.height:
                screen_x, screen_y = camera.world_to_screen(x * TILE_SIZE, y * TILE_SIZE)
                rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                
                # Create semi-transparent surface for preview
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.set_alpha(128)
                s.fill(self.cable_color)
                screen.blit(s, (screen_x, screen_y))
                pygame.draw.rect(screen, (0, 0, 0), rect, 1) 