import pygame
from .base_renderer import BaseRenderer
from world.modules import LifeSupportModule, ReactorModule, EngineModule, DockingDoorModule

class ModuleRenderer(BaseRenderer):
    def draw_modules(self, screen, deck, camera):
        """Draw all modules and their power status"""
        tile_size = self.get_scaled_size(camera)
        
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                if not tile.module:
                    continue
                    
                screen_x, screen_y = self.get_screen_position(camera, x, y)
                self._draw_module(screen, tile.module, screen_x, screen_y, tile_size)
                self._draw_power_status(screen, tile.module, screen_x, screen_y, tile_size, camera)

    def _draw_module(self, screen, module, x, y, size):
        """Draw a specific module"""
        image_key = None
        if isinstance(module, LifeSupportModule):
            image_key = 'life_support'
        elif isinstance(module, ReactorModule):
            image_key = 'reactor'
        elif isinstance(module, EngineModule):
            image_key = 'engine'
        elif isinstance(module, DockingDoorModule):
            # Only draw at primary position
            if (x // size, y // size) == module.primary_position:
                image_key = 'docking_door'
                if module.direction == 'horizontal':
                    size = (size * 2, size)  # Double width
                else:
                    size = (size, size * 2)  # Double height
        
        if image_key:
            image = self.asset_loader.get_image(image_key)
            if image:
                scaled_image = pygame.transform.scale(image, size if isinstance(size, tuple) else (size, size))
                if not module.is_powered():
                    tinted = scaled_image.copy()
                    tinted.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(tinted, (x, y))
                else:
                    screen.blit(scaled_image, (x, y))

    def _draw_power_status(self, screen, module, x, y, size, camera):
        """Draw power status text for a module"""
        font_size = int(20 * camera.zoom)
        font = pygame.font.Font(None, max(10, font_size))
        
        if isinstance(module, ReactorModule):
            text = f"+{module.power_output}"
            text_color = (100, 255, 100)
        else:
            if module.is_powered():
                text = f"{module.power_available}/{module.power_required}"
                text_color = (100, 255, 100)
            else:
                text = f"0/{module.power_required}"
                text_color = (255, 50, 50)
                
        self._draw_outlined_text(screen, text, font, text_color, x + size//2, y + size//2)

    def _draw_outlined_text(self, screen, text, font, color, x, y):
        """Draw text with outline and background"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Draw background
        padding = 2
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 160))
        screen.blit(bg_surface, bg_rect)
        
        # Draw outline
        outline_positions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in outline_positions:
            screen.blit(font.render(text, True, (0, 0, 0)), 
                       text_rect.move(dx, dy))
        
        # Draw main text
        screen.blit(text_surface, text_rect) 