import pygame

class TimeUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_time_controls(self, screen, time_manager, x, y):
        # Draw time background
        pygame.draw.rect(screen, (30, 30, 30), (x, y, 160, 50))
        pygame.draw.rect(screen, (100, 200, 255), (x, y, 160, 50), 2)
        
        # Draw clock
        time_text = time_manager.get_time_string()
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (x + 10, y + 5))
        
        # Draw speed indicator
        speed_text = f"{'⏸' if time_manager.paused else '⏵'} {time_manager.time_scale}x"
        speed_surface = self.small_font.render(speed_text, True, (200, 200, 200))
        screen.blit(speed_surface, (x + 10, y + 30)) 