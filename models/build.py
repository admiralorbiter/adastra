from enum import Enum, auto
from dataclasses import dataclass
import pygame

class BuildMode(Enum):
    NONE = auto()
    FLOOR = auto()
    WALL = auto()
    MODULE = auto()
    OBJECT = auto()

@dataclass
class BuildableItem:
    name: str
    description: str
    icon_color: tuple[int, int, int]  # RGB color tuple
    cost: int = 10
    
    def can_build(self, ship, x: int, y: int) -> bool:
        """Check if item can be built at the specified location"""
        if not ship.decks:
            return False
        deck = ship.decks[0]
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
        return True

class BuildCategory:
    def __init__(self, mode: BuildMode, items: list[BuildableItem]):
        self.mode = mode
        self.items = items
        self.selected_item: BuildableItem | None = None

class BuildSystem:
    def __init__(self):
        self.current_mode = BuildMode.NONE
        self.categories = {
            BuildMode.FLOOR: BuildCategory(BuildMode.FLOOR, [
                BuildableItem("Basic Floor", "A simple metal floor", (200, 200, 200)),
                BuildableItem("Advanced Floor", "High-tech composite floor", (220, 220, 220))
            ]),
            BuildMode.WALL: BuildCategory(BuildMode.WALL, [
                BuildableItem("Basic Wall", "Standard wall panel", (100, 100, 100)),
                BuildableItem("Reinforced Wall", "Stronger wall panel", (120, 120, 120))
            ]),
            BuildMode.MODULE: BuildCategory(BuildMode.MODULE, [
                BuildableItem("Life Support", "Provides oxygen", (100, 100, 255)),
                BuildableItem("Reactor", "Generates power", (255, 100, 100))
            ]),
            BuildMode.OBJECT: BuildCategory(BuildMode.OBJECT, [
                BuildableItem("Bed", "Crew sleeping quarters", (139, 69, 19)),
                BuildableItem("Storage", "Storage container", (255, 255, 0))
            ])
        }
        self.active_category: BuildCategory | None = None

    def set_mode(self, mode: BuildMode) -> None:
        if self.current_mode == mode:
            self.current_mode = BuildMode.NONE
            self.active_category = None
        else:
            self.current_mode = mode
            self.active_category = self.categories.get(mode)

    def get_current_item(self) -> BuildableItem | None:
        if self.active_category:
            return self.active_category.selected_item
        return None

class BuildUI:
    def __init__(self, screen_width: int):
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

    def handle_click(self, pos: tuple[int, int]) -> bool:
        for mode, button in self.buttons.items():
            if button.is_clicked(pos):
                self.build_system.set_mode(mode)
                button.active = (self.build_system.current_mode == mode)
                # Deactivate other buttons
                for other_button in self.buttons.values():
                    if other_button != button:
                        other_button.active = False
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