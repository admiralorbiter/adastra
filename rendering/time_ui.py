import pygame

class TimeUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_time_controls(self, screen, time_manager, build_ui):
        # Position relative to build UI
        x = build_ui.x - 130  # 10px gap between build UI and time UI
        y = build_ui.y  # Align with top of build UI
        
        # Draw time background - made compact
        bg_width = 120
        bg_height = 40
        pygame.draw.rect(screen, (30, 30, 30), (x, y, bg_width, bg_height))
        pygame.draw.rect(screen, (100, 200, 255), (x, y, bg_width, bg_height), 2)
        
        # Draw clock - smaller font
        time_text = time_manager.get_time_string()
        text_surface = self.small_font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (x + 8, y + 5))
        
        # Draw speed indicator with pause state
        if time_manager.paused:
            speed_text = "⏸ PAUSED"
        else:
            speed_text = f"⏵ {time_manager.time_scale:.1f}x"
            
        speed_surface = self.small_font.render(speed_text, True, (200, 200, 200))
        screen.blit(speed_surface, (x + 8, y + 22)) 