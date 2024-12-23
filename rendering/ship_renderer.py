import pygame

from world.items import ItemType
from world.modules import LifeSupportModule, ReactorModule, EngineModule
from world.objects import Bed, StorageContainer, Tank
from rendering.asset_loader import AssetLoader
from utils.constants import GameConstants

class ShipRenderer:
    @staticmethod
    def draw_ship(screen, ship, camera, selected_crew=None, build_ui=None):
        if not ship.decks:
            return

        deck = ship.decks[0]
        tile_size = int(GameConstants.get_instance().TILE_SIZE * camera.zoom)  # Scale tile size based on zoom level
        
        # Get current build item if in build mode and build_ui exists
        current_item = build_ui.build_system.get_current_item() if build_ui else None

        asset_loader = AssetLoader.get_instance()
        
        # First pass: Draw tiles and modules
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                screen_x, screen_y = camera.world_to_screen(x * GameConstants.get_instance().TILE_SIZE, y * GameConstants.get_instance().TILE_SIZE)
                rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                
                # Draw the tile
                color = (200, 200, 200)  # Default floor color
                if tile.wall:
                    color = (50, 50, 50)  # Wall color
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border
                
                # Then draw objects and modules on top
                if tile.object:
                    if isinstance(tile.object, Bed):
                        image = asset_loader.get_image('bed')
                        if image:
                            scaled_image = pygame.transform.scale(image, (tile_size, tile_size))
                            screen.blit(scaled_image, (screen_x, screen_y))
                        else:
                            color = (139, 69, 19)  # Brown fallback for bed
                            pygame.draw.rect(screen, color, rect)
                            
                    elif isinstance(tile.object, StorageContainer):
                        image = asset_loader.get_image('container')
                        if image:
                            scaled_image = pygame.transform.scale(image, (tile_size, tile_size))
                            screen.blit(scaled_image, (screen_x, screen_y))
                        else:
                            color = (255, 255, 0)  # Yellow fallback for storage
                            pygame.draw.rect(screen, color, rect)
                            
                    elif isinstance(tile.object, Tank):
                        # Draw tank with different color based on contents
                        if tile.object.get_amount(ItemType.OXYGEN) > 0:
                            color = (100, 100, 255)  # Blue for oxygen
                        elif tile.object.get_amount(ItemType.WATER) > 0:
                            color = (0, 191, 255)  # Light blue for water
                        else:
                            color = (150, 150, 150)  # Gray for empty tank
                        pygame.draw.rect(screen, color, rect)
                        
                    # Draw border for objects
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
                        text_color = (100, 255, 100)  # Lighter green
                    else:
                        if tile.module.is_powered():
                            text = f"{tile.module.power_available}/{tile.module.power_required}"
                            text_color = (100, 255, 100)  # Lighter green
                        else:
                            text = f"0/{tile.module.power_required}"
                            text_color = (255, 50, 50)
                    
                    # Create text surface with outline
                    def create_outlined_text(text, font, text_color, outline_color=(0, 0, 0)):
                        # Create the outline by rendering the text multiple times with offsets
                        outline_surfaces = []
                        outline_positions = [(-1,-1), (-1,1), (1,-1), (1,1)]  # Diagonal positions
                        
                        # Create outline pieces
                        for dx, dy in outline_positions:
                            outline_surface = font.render(text, True, outline_color)
                            outline_surfaces.append((outline_surface, (dx, dy)))
                        
                        # Create main text
                        text_surface = font.render(text, True, text_color)
                        
                        # Calculate the size needed for the combined surface
                        width = text_surface.get_width() + 2  # Add 2 for outline
                        height = text_surface.get_height() + 2  # Add 2 for outline
                        
                        # Create final surface with alpha channel
                        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        
                        # Blit outline pieces
                        for surface, (dx, dy) in outline_surfaces:
                            final_surface.blit(surface, (dx + 1, dy + 1))  # +1 to center
                        
                        # Blit main text in center
                        final_surface.blit(text_surface, (1, 1))  # Center the main text
                        
                        return final_surface
                    
                    # Create the outlined text surface
                    text_surface = create_outlined_text(text, font, text_color)
                    text_rect = text_surface.get_rect(center=(screen_x + tile_size//2, screen_y + tile_size//2))
                    
                    # Create slightly larger background rect
                    padding = 2
                    bg_rect = text_rect.inflate(padding * 2, padding * 2)
                    
                    # Draw semi-transparent white background
                    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                    bg_surface.fill((255, 255, 255, 160))  # White with 60% opacity (slightly more transparent)
                    screen.blit(bg_surface, bg_rect)
                    
                    # Draw the outlined text
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
                crew_member.x * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2,
                crew_member.y * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2
            )
            radius = int((GameConstants.get_instance().TILE_SIZE//3) * camera.zoom)
            pygame.draw.circle(screen, (0, 255, 0), (screen_x, screen_y), radius)

        # Draw selected crew highlight with scaled size
        if selected_crew:
            screen_x, screen_y = camera.world_to_screen(
                selected_crew.x * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2,
                selected_crew.y * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2
            )
            radius = int((GameConstants.get_instance().TILE_SIZE//2) * camera.zoom)
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), max(1, int(2 * camera.zoom)))

            if selected_crew.move_path:
                path_points = []
                start_x, start_y = camera.world_to_screen(
                    selected_crew.x * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2,
                    selected_crew.y * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2
                )
                path_points.append((start_x, start_y))
                
                for x, y in selected_crew.move_path:
                    screen_x, screen_y = camera.world_to_screen(
                        x * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2,
                        y * GameConstants.get_instance().TILE_SIZE + GameConstants.get_instance().TILE_SIZE // 2
                    )
                    path_points.append((screen_x, screen_y))
                pygame.draw.lines(screen, (255, 255, 0), False, path_points, 2)

        # Draw bed highlight if crew is selected
        if selected_crew:
            for y in range(deck.height):
                for x in range(deck.width):
                    tile = deck.tiles[y][x]
                    if tile and tile.object and isinstance(tile.object, Bed):
                        screen_x, screen_y = camera.world_to_screen(x * GameConstants.get_instance().TILE_SIZE, y * GameConstants.get_instance().TILE_SIZE)
                        tile_size = int(GameConstants.get_instance().TILE_SIZE * camera.zoom)
                        pygame.draw.rect(screen, (0, 255, 255, 128), 
                                       (screen_x, screen_y, tile_size, tile_size), 2)

        # Draw base tiles first
        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                screen_x, screen_y = camera.world_to_screen(x * GameConstants.get_instance().TILE_SIZE, y * GameConstants.get_instance().TILE_SIZE)
                
                # Highlight beds if crew is selected
                if selected_crew and tile.object and isinstance(tile.object, Bed):
                    pygame.draw.rect(screen, (0, 255, 255), 
                                   (screen_x, screen_y, tile_size, tile_size), 2)
        
        # Draw crew members
        for crew in ship.crew:
            screen_x, screen_y = camera.world_to_screen(crew.x * GameConstants.get_instance().TILE_SIZE, crew.y * GameConstants.get_instance().TILE_SIZE)
            color = (0, 255, 0)  # Default color
            if crew == selected_crew:
                # Draw selection highlight
                pygame.draw.rect(screen, (255, 255, 0),
                               (screen_x, screen_y, tile_size, tile_size), 2)