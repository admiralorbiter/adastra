import pygame

from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
from rendering.asset_loader import AssetLoader

TILE_SIZE = 32

class ShipRenderer:
    @staticmethod
    def draw_ship(screen, ship, camera, selected_crew=None, build_ui=None):
        if not ship.decks:
            return

        deck = ship.decks[0]
        tile_size = int(32 * camera.zoom)  # Scale tile size based on zoom level
        
        # Get current build item if in build mode and build_ui exists
        current_item = build_ui.build_system.get_current_item() if build_ui else None

        asset_loader = AssetLoader.get_instance()
        
        # First pass: Draw tiles and modules
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                screen_x, screen_y = camera.world_to_screen(x * 32, y * 32)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                # Draw the tile
                color = (200, 200, 200)  # Default floor color
                
                if tile.wall:
                    color = (50, 50, 50)  # Wall color
                elif tile.module:
                    # Differentiate modules by type:
                    if isinstance(tile.module, LifeSupportModule):
                        # Red if unpowered, blue if powered
                        if tile.module.is_powered():
                            color = (100, 100, 255)  # Blueish for powered Life Support
                        else:
                            color = (255, 100, 100)  # Reddish for unpowered Life Support
                    elif isinstance(tile.module, ReactorModule):
                        color = (255, 140, 0)  # Orange for Reactor
                elif tile.object:
                    # Differentiate objects by class:
                    if isinstance(tile.object, Bed):
                        color = (139, 69, 19)  # Brown for bed
                    elif isinstance(tile.object, StorageContainer):
                        color = (255, 255, 0)  # Yellow for storage

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                # Draw modules with scaled images
                if tile.module:
                    if isinstance(tile.module, LifeSupportModule):
                        image = asset_loader.get_image('life_support')
                        # Scale image to match zoom level
                        scaled_image = pygame.transform.scale(image, (tile_size, tile_size))
                        if not tile.module.is_powered():
                            tinted = scaled_image.copy()
                            tinted.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                            screen.blit(tinted, (screen_x, screen_y))
                        else:
                            screen.blit(scaled_image, (screen_x, screen_y))
                    elif isinstance(tile.module, ReactorModule):
                        image = asset_loader.get_image('reactor')
                        scaled_image = pygame.transform.scale(image, (tile_size, tile_size))
                        screen.blit(scaled_image, (screen_x, screen_y))
                
                # Draw power status with scaled text
                if tile.module:
                    # Scale font size with zoom
                    font_size = int(20 * camera.zoom)
                    font = pygame.font.Font(None, max(10, font_size))
                    
                    if isinstance(tile.module, ReactorModule):
                        text = f"+{tile.module.power_output}"
                        text_color = (0, 255, 0)
                    else:
                        if tile.module.is_powered():
                            text = f"{tile.module.power_available}/{tile.module.power_required}"
                            text_color = (0, 255, 0)
                        else:
                            text = f"0/{tile.module.power_required}"
                            text_color = (255, 50, 50)
                    
                    text_surface = font.render(text, True, text_color)
                    text_rect = text_surface.get_rect(center=(screen_x + tile_size//2, screen_y + tile_size//2))
                    screen.blit(text_surface, text_rect)

                # Highlight valid build locations when in build mode
                if current_item and current_item.can_build(ship, x, y):
                    # Create scaled highlight surface
                    s = pygame.Surface((tile_size, tile_size))
                    s.set_alpha(128)
                    s.fill((0, 255, 0))
                    screen.blit(s, (screen_x, screen_y))

        # Draw crew members with scaled size
        for crew_member in ship.crew:
            screen_x, screen_y = camera.world_to_screen(
                crew_member.x * 32 + 16,
                crew_member.y * 32 + 16
            )
            radius = int((TILE_SIZE//3) * camera.zoom)
            pygame.draw.circle(screen, (0, 255, 0), (screen_x, screen_y), radius)

        # Draw selected crew highlight with scaled size
        if selected_crew:
            screen_x, screen_y = camera.world_to_screen(
                selected_crew.x * 32 + 16,
                selected_crew.y * 32 + 16
            )
            radius = int((TILE_SIZE//2) * camera.zoom)
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), max(1, int(2 * camera.zoom)))

            if selected_crew.move_path:
                path_points = []
                start_x, start_y = camera.world_to_screen(
                    selected_crew.x * TILE_SIZE + TILE_SIZE // 2,
                    selected_crew.y * TILE_SIZE + TILE_SIZE // 2
                )
                path_points.append((start_x, start_y))
                
                for x, y in selected_crew.move_path:
                    screen_x, screen_y = camera.world_to_screen(
                        x * TILE_SIZE + TILE_SIZE // 2,
                        y * TILE_SIZE + TILE_SIZE // 2
                    )
                    path_points.append((screen_x, screen_y))
                pygame.draw.lines(screen, (255, 255, 0), False, path_points, 2)