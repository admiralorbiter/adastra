from enum import Enum, auto
from dataclasses import dataclass
import pygame

from world.objects import Bed, StorageContainer
from world.tile import Tile

class BuildMode(Enum):
    NONE = auto()
    FLOOR = auto()
    WALL = auto()
    CABLE = auto()
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
        
        # For wall, allow building within bounds or one tile beyond
        if self.name == "Basic Wall":
            # Allow building one tile beyond in any direction
            if not (-1 <= x <= deck.width and -1 <= y <= deck.height):
                return False
            
            # If within bounds, check if tile is empty
            if 0 <= x < deck.width and 0 <= y < deck.height:
                tile = deck.tiles[y][x]
                if tile.wall or tile.module or tile.object:
                    return False
                
            # Must be adjacent to existing tile
            adjacent_coords = [
                (ax, ay) for ax, ay in [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1)
                ] if 0 <= ax < deck.width and 0 <= ay < deck.height
            ]
            return len(adjacent_coords) > 0
        
        # For other items, check normal bounds
        if not (0 <= x < deck.width and 0 <= y < deck.height):
            return False
        
        return True

    def build(self, ship, x: int, y: int) -> bool:
        """Actually perform the building action"""
        if not self.can_build(ship, x, y):
            return False
            
        deck = ship.decks[0]
        
        # Handle wall placement with expansion
        if self.name == "Basic Wall":
            # Handle expansion cases
            if x == deck.width:
                ship.expand_deck("right", y=y)
                return True
            elif x == -1:
                ship.expand_deck("left", y=y)
                return True
            elif y == deck.height:
                ship.expand_deck("down", x=x)
                return True
            elif y == -1:
                ship.expand_deck("up", x=x)
                return True
            
            # Place single wall within bounds
            if 0 <= x < deck.width and 0 <= y < deck.height:
                # Ensure tile exists before setting wall
                if not deck.tiles[y][x]:
                    deck.tiles[y][x] = Tile(x=x, y=y)
                deck.tiles[y][x].wall = True
                return True
        
        # Handle other building types...
        elif self.name == "Basic Floor":
            if not deck.tiles[y][x]:
                deck.tiles[y][x] = Tile(x=x, y=y)
            deck.tiles[y][x].wall = False
            return True
        elif self.name == "Bed":
            deck.tiles[y][x].object = Bed()
            return True
        elif self.name == "Storage Container":
            deck.tiles[y][x].object = StorageContainer()
            return True
        elif self.name == "Power Cable":
            ship.cable_system.add_cable(x, y)
            return True
        
        return False

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
            ]),
            BuildMode.WALL: BuildCategory(BuildMode.WALL, [
                BuildableItem("Basic Wall", "Standard wall panel", (100, 100, 100)),
            ]),
            BuildMode.CABLE: BuildCategory(BuildMode.CABLE, [
                BuildableItem("Power Cable", "Basic power cable", (255, 140, 0)),
            ]),
            BuildMode.OBJECT: BuildCategory(BuildMode.OBJECT, [
                BuildableItem("Bed", "A place for crew to rest", (139, 69, 19)),
                BuildableItem("Storage Container", "Store items and resources", (160, 82, 45))
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
            if self.active_category:
                self.active_category.selected_item = self.active_category.items[0]

    def get_current_item(self) -> BuildableItem | None:
        if self.active_category:
            return self.active_category.selected_item
        return None

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

    def handle_click(self, pos: tuple[int, int]) -> bool:
        # Handle main button clicks
        for mode, button in self.buttons.items():
            if button.is_clicked(pos):
                self.build_system.set_mode(mode)
                button.active = (self.build_system.current_mode == mode)
                
                # Show object menu when Object mode is selected
                if mode == BuildMode.OBJECT:
                    self.show_object_menu = button.active
                    self.selected_item = None
                else:
                    self.show_object_menu = False
                
                # Deactivate other buttons
                for other_button in self.buttons.values():
                    if other_button != button:
                        other_button.active = False
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

        # Draw cable mode highlights if active
        if self.build_system.current_mode == BuildMode.CABLE:
            # Get mouse position and convert to grid coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x, world_y = self.game_state.camera.screen_to_world(mouse_x, mouse_y)
            grid_x = int(world_x / 32)
            grid_y = int(world_y / 32)

            # Only highlight if mouse is over valid grid position
            if (0 <= grid_x < self.game_state.ship.decks[0].width and 
                0 <= grid_y < self.game_state.ship.decks[0].height):
                
                # Convert grid position back to screen coordinates
                screen_x, screen_y = self.game_state.camera.world_to_screen(grid_x * 32, grid_y * 32)
                tile_size = int(32 * self.game_state.camera.zoom)
                
                # Create highlight surface with proper scaling
                highlight = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                highlight.fill(self.highlight_color)
                screen.blit(highlight, (screen_x, screen_y))
                
                # Draw scaled border
                border_width = max(1, int(self.game_state.camera.zoom))
                pygame.draw.rect(screen, (100, 200, 255), 
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