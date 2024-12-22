import pygame

class ResourceUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_oxygen_status(self, screen, ship, x, y):
        # Draw O2 bar background
        bar_width = 200
        bar_height = 30
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # Draw O2 bar fill
        fill_width = int((ship.global_oxygen / ship.oxygen_capacity) * bar_width)
        o2_color = self._get_oxygen_color(ship.global_oxygen / ship.oxygen_capacity)
        pygame.draw.rect(screen, o2_color, (x, y, fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (x, y, bar_width, bar_height), 2)
        
        # Draw text
        o2_text = f"O₂: {int(ship.global_oxygen)}/{int(ship.oxygen_capacity)}"
        text_surface = self.font.render(o2_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(x + 10, y + bar_height // 2))
        screen.blit(text_surface, text_rect)
        
        # Draw consumption rate
        consumption_text = f"Usage: {len(ship.crew) * ship.oxygen_consumption_per_crew:.1f}/s"
        consumption_surface = self.small_font.render(consumption_text, True, (200, 200, 200))
        screen.blit(consumption_surface, (x, y + bar_height + 5))
    
    def _get_oxygen_color(self, percentage):
        if percentage > 0.6:
            return (0, 255, 0)  # Green
        elif percentage > 0.3:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red 