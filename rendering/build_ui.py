import pygame
from models.builders.build import BuildMode, BuildSystem
from utils.constants import GameConstants

class BuildUI:
    def __init__(self, screen_width: int, game_state):
        self.game_state = game_state
        self.build_system = BuildSystem()
        self.button_size = 40
        self.margin = 10
        self.panel_width = 200
        self.panel_height = 250
        
        # Position panel in top-right corner
        self.x = screen_width - self.panel_width - 20
        self.y = 20  # Add some top margin
        
        # Create buttons with proper spacing
        self.buttons = {}
        y_pos = self.y + self.margin
        for mode in BuildMode:
            if mode != BuildMode.NONE:
                category = self.build_system.categories.get(mode)
                if category and category.items:
                    first_item = category.items[0]
                    self.buttons[mode] = UIButton(
                        pygame.Rect(self.x + self.margin, y_pos, self.button_size, self.button_size),
                        mode.name.title(),
                        first_item.icon_color,
                        f"Build {mode.name.title()}"
                    )
                    y_pos += self.button_size + self.margin

        self.highlight_color = (100, 200, 255, 128)  # Light blue with alpha
        self.selected_item = None
        self.show_object_menu = False
        self.object_menu_rect = pygame.Rect(
            self.x, 
            self.y + self.panel_height + 10, 
            self.panel_width, 
            100
        )
        self.show_module_menu = False
        self.module_menu_rect = pygame.Rect(
            self.x, 
            self.y + self.panel_height + 10, 
            self.panel_width, 
            100
        )

    def handle_click(self, pos: tuple[int, int]) -> bool:
        # Handle main button clicks
        for mode, button in self.buttons.items():
            if button.is_clicked(pos):
                self.build_system.set_mode(mode)
                button.active = (self.build_system.current_mode == mode)
                
                # Show appropriate menu based on mode
                if mode == BuildMode.OBJECT:
                    self.show_object_menu = button.active
                    self.show_module_menu = False
                    self.selected_item = None
                elif mode == BuildMode.MODULE:
                    self.show_module_menu = button.active
                    self.show_object_menu = False
                    self.selected_item = None
                else:
                    self.show_object_menu = False
                    self.show_module_menu = False
                
                # Deactivate other buttons
                for other_button in self.buttons.values():
                    if other_button != button:
                        other_button.active = False
                return True

        # Handle module menu clicks if visible
        if self.show_module_menu:
            category = self.build_system.categories[BuildMode.MODULE]
            item_height = 30
            for i, item in enumerate(category.items):
                item_rect = pygame.Rect(
                    self.module_menu_rect.x,
                    self.module_menu_rect.y + i * item_height,
                    self.module_menu_rect.width,
                    item_height
                )
                if item_rect.collidepoint(pos):
                    self.selected_item = item
                    category.selected_item = item
                    return True

        # Handle object menu clicks if visible
        if self.show_object_menu:
            category = self.build_system.categories[BuildMode.OBJECT]
            item_height = 30
            for i, item in enumerate(category.items):
                item_rect = pygame.Rect(
                    self.object_menu_rect.x,
                    self.object_menu_rect.y + i * item_height,
                    self.object_menu_rect.width,
                    item_height
                )
                if item_rect.collidepoint(pos):
                    self.selected_item = item
                    category.selected_item = item
                    return True

        return False

    def draw(self, screen: pygame.Surface) -> None:
        # Draw main panel background with border
        panel_rect = pygame.Rect(self.x, self.y, self.panel_width, self.panel_height)
        
        # Semi-transparent background
        s = pygame.Surface((panel_rect.width, panel_rect.height))
        s.set_alpha(128)
        s.fill((30, 30, 30))
        screen.blit(s, (panel_rect.x, panel_rect.y))
        
        # Draw panel border (light blue like O2 meter)
        pygame.draw.rect(screen, (100, 200, 255), panel_rect, 2)
        
        # Draw buttons and labels
        font = pygame.font.Font(None, 24)
        for mode, button in self.buttons.items():
            button.draw(screen)
            
            # Draw label to the right of button
            label = font.render(mode.name.title(), True, (200, 200, 200))
            label_x = button.rect.right + 10
            label_y = button.rect.centery - label.get_height() // 2
            screen.blit(label, (label_x, label_y))

        # Draw build mode highlights if active
        current_item = self.build_system.get_current_item()
        if current_item and self.build_system.current_mode in [BuildMode.FLOOR, BuildMode.WALL, BuildMode.CABLE]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)

            # Check if position is valid for building
            can_build = current_item.can_build(self.game_state.ship, grid_x, grid_y)
            highlight_color = (0, 255, 0, 128) if can_build else (255, 0, 0, 128)

            # Only highlight if mouse is over valid grid position
            if (-1 <= grid_x <= self.game_state.ship.decks[0].width and 
                -1 <= grid_y <= self.game_state.ship.decks[0].height):
                
                # Convert grid position back to screen coordinates
                screen_x, screen_y = self.game_state.camera.grid_to_screen(grid_x, grid_y)
                tile_size = int(GameConstants.get_instance().TILE_SIZE * self.game_state.camera.zoom)
                
                # Create highlight surface with proper scaling
                highlight = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                highlight.fill(highlight_color)
                screen.blit(highlight, (screen_x, screen_y))
                
                # Draw scaled border
                border_width = max(1, int(self.game_state.camera.zoom))
                border_color = (0, 255, 0) if can_build else (255, 0, 0)
                pygame.draw.rect(screen, border_color, 
                               pygame.Rect(screen_x, screen_y, tile_size, tile_size), 
                               border_width)

        # Draw object menu if visible
        if self.show_object_menu:
            # Draw menu background
            s = pygame.Surface((self.object_menu_rect.width, self.object_menu_rect.height))
            s.set_alpha(128)
            s.fill((30, 30, 30))
            screen.blit(s, (self.object_menu_rect.x, self.object_menu_rect.y))
            
            # Draw menu border
            pygame.draw.rect(screen, (100, 200, 255), self.object_menu_rect, 2)
            
            # Draw object items
            font = pygame.font.Font(None, 24)
            item_height = 30
            for i, item in enumerate(self.build_system.categories[BuildMode.OBJECT].items):
                item_rect = pygame.Rect(
                    self.object_menu_rect.x,
                    self.object_menu_rect.y + i * item_height,
                    self.object_menu_rect.width,
                    item_height
                )
                
                # Highlight selected item
                if item == self.selected_item:
                    pygame.draw.rect(screen, (60, 60, 60), item_rect)
                
                # Draw item icon
                icon_rect = pygame.Rect(
                    item_rect.x + 5,
                    item_rect.y + 5,
                    20,
                    20
                )
                pygame.draw.rect(screen, item.icon_color, icon_rect)
                
                # Draw item name
                text = font.render(item.name, True, (200, 200, 200))
                screen.blit(text, (icon_rect.right + 10, item_rect.centery - text.get_height()//2))

        # Draw module menu if visible
        if self.show_module_menu:
            # Draw menu background
            s = pygame.Surface((self.module_menu_rect.width, self.module_menu_rect.height))
            s.set_alpha(128)
            s.fill((30, 30, 30))
            screen.blit(s, (self.module_menu_rect.x, self.module_menu_rect.y))
            
            # Draw menu border
            pygame.draw.rect(screen, (100, 200, 255), self.module_menu_rect, 2)
            
            # Draw module items
            font = pygame.font.Font(None, 24)
            item_height = 30
            for i, item in enumerate(self.build_system.categories[BuildMode.MODULE].items):
                item_rect = pygame.Rect(
                    self.module_menu_rect.x,
                    self.module_menu_rect.y + i * item_height,
                    self.module_menu_rect.width,
                    item_height
                )
                
                # Highlight selected item
                if item == self.selected_item:
                    pygame.draw.rect(screen, (60, 60, 60), item_rect)
                
                # Draw item icon
                icon_rect = pygame.Rect(
                    item_rect.x + 5,
                    item_rect.y + 5,
                    20,
                    20
                )
                pygame.draw.rect(screen, item.icon_color, icon_rect)
                
                # Draw item name
                text = font.render(item.name, True, (200, 200, 200))
                screen.blit(text, (icon_rect.right + 10, item_rect.centery - text.get_height()//2))

    def clear_selection(self):
        """Clear all selections and menus"""
        self.build_system.clear_selection()
        self.show_object_menu = False
        self.show_module_menu = False
        self.selected_item = None
        # Deactivate all buttons
        for button in self.buttons.values():
            button.active = False

class UIButton:
    def __init__(self, rect: pygame.Rect, text: str, icon_color: tuple[int, int, int], tooltip: str = ""):
        self.rect = rect
        self.text = text
        self.icon_color = icon_color
        self.tooltip = tooltip
        self.active = False

    def draw(self, screen: pygame.Surface) -> None:
        # Draw button background
        bg_color = (60, 60, 60) if not self.active else (100, 100, 100)
        pygame.draw.rect(screen, bg_color, self.rect)
        
        # Draw icon
        padding = 6
        icon_rect = pygame.Rect(
            self.rect.x + padding,
            self.rect.y + padding,
            self.rect.width - padding * 2,
            self.rect.height - padding * 2
        )
        pygame.draw.rect(screen, self.icon_color, icon_rect)
        
        # Draw button border
        border_color = (100, 200, 255) if self.active else (150, 150, 150)
        pygame.draw.rect(screen, border_color, self.rect, 2)

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos) 