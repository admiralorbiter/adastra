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
        tile_size = int(TILE_SIZE * camera.zoom)
        
        # Draw existing cables
        for (x, y), cable in cable_system.cables.items():
            if 0 <= x < deck.width and 0 <= y < deck.height:
                # Convert grid coordinates to world coordinates
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                # Convert world coordinates to screen coordinates
                screen_x, screen_y = camera.world_to_screen(world_x, world_y)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                # Draw cable with scaled border
                pygame.draw.rect(screen, self.cable_color, rect)
                border_width = max(1, int(camera.zoom))
                pygame.draw.rect(screen, (0, 0, 0), rect, border_width)
                
                # Draw power indicator
                if cable.powered:
                    indicator_size = max(4, int(4 * camera.zoom))
                    indicator_pos = (
                        screen_x + tile_size // 2 - indicator_size // 2,
                        screen_y + tile_size // 2 - indicator_size // 2
                    )
                    pygame.draw.rect(screen, (255, 255, 0), 
                                   pygame.Rect(indicator_pos, (indicator_size, indicator_size)))
        
        # Draw preview cables
        for x, y in cable_system.preview_cables:
            if 0 <= x < deck.width and 0 <= y < deck.height:
                # Convert grid coordinates to world coordinates
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                # Convert world coordinates to screen coordinates
                screen_x, screen_y = camera.world_to_screen(world_x, world_y)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                # Create scaled semi-transparent preview
                s = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                s.fill((255, 140, 0, 128))  # Semi-transparent orange
                screen.blit(s, (screen_x, screen_y))
                
                # Draw scaled border
                border_width = max(1, int(camera.zoom))
                pygame.draw.rect(screen, (0, 0, 0), rect, border_width) 