import pygame

class ResourceUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_oxygen_status(self, screen, ship, x, y):
        # Draw O2 bar background
        bar_width = 160  # Made slightly smaller
        bar_height = 24  # Made slightly smaller
        
        # Draw oxygen bar
        self._draw_resource_bar(
            screen, 
            "O₂", 
            ship.global_oxygen, 
            ship.oxygen_capacity,
            f"Usage: {len(ship.crew) * ship.oxygen_consumption_per_crew:.1f}/s",
            x, y, 
            bar_width, 
            bar_height
        )
        
        # Calculate average crew hunger
        if ship.crew:
            avg_hunger = sum(crew.hunger for crew in ship.crew) / len(ship.crew)
        else:
            avg_hunger = 100
            
        # Draw hunger bar below oxygen
        self._draw_resource_bar(
            screen,
            "Hunger",
            avg_hunger,  # Current hunger level
            100,        # Maximum hunger level
            f"Crew: {len(ship.crew)}",
            x, y + bar_height + 15,  # Positioned below oxygen bar
            bar_width,
            bar_height
        )
    
    def _draw_resource_bar(self, screen, label, current, maximum, usage_text, x, y, width, height):
        # Draw bar background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        
        # Draw fill
        percentage = current / maximum
        fill_width = int(percentage * width)
        color = self._get_resource_color(percentage)
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)
        
        # Draw text
        text = f"{label}: {int(current)}/{int(maximum)}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(x + 10, y + height // 2))
        screen.blit(text_surface, text_rect)
        
        # Draw usage rate
        usage_surface = self.small_font.render(usage_text, True, (200, 200, 200))
        screen.blit(usage_surface, (x, y + height + 2))
    
    def _get_resource_color(self, percentage):
        if percentage > 0.6:
            return (0, 255, 0)  # Green
        elif percentage > 0.3:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red