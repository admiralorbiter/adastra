import pygame

from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer

TILE_SIZE = 32

class ShipRenderer:
    @staticmethod
    def draw_ship(screen, ship, camera, selected_crew=None, build_ui=None):
        if not ship.decks:
            return

        deck = ship.decks[0]
        
        # Get current build item if in build mode and build_ui exists
        current_item = build_ui.build_system.get_current_item() if build_ui else None

        for y in range(deck.height):
            for x in range(deck.width):
                tile = deck.tiles[y][x]
                color = (200, 200, 200)  # Default floor color
                
                if tile.wall:
                    color = (50, 50, 50)  # Wall color
                elif tile.module:
                    # Differentiate modules by type:
                    if isinstance(tile.module, LifeSupportModule):
                        color = (100, 100, 255)  # Blueish for Life Support
                    elif isinstance(tile.module, ReactorModule):
                        color = (255, 100, 100)  # Reddish for Reactor
                elif tile.object:
                    # Differentiate objects by class:
                    if isinstance(tile.object, Bed):
                        color = (139, 69, 19)  # Brown for bed
                    elif isinstance(tile.object, StorageContainer):
                        color = (255, 255, 0)  # Yellow for storage

                # Highlight valid build locations when in build mode
                if current_item:
                    if current_item.can_build(ship, x, y):
                        # Add a green tint to show valid build location
                        r, g, b = color
                        color = (min(255, r + 50), min(255, g + 100), b)

                # Use camera to convert world position to screen position
                screen_x, screen_y = camera.world_to_screen(x * TILE_SIZE, y * TILE_SIZE)
                rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)
                
                # Draw valid build locations with a green outline
                if current_item and current_item.can_build(ship, x, y):
                    pygame.draw.rect(screen, (0, 255, 0), rect, 2)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Draw crew members
        for crew_member in ship.crew:
            screen_x, screen_y = camera.world_to_screen(
                crew_member.x * TILE_SIZE + TILE_SIZE // 2,
                crew_member.y * TILE_SIZE + TILE_SIZE // 2
            )
            radius = TILE_SIZE // 3
            pygame.draw.circle(screen, (0, 255, 0), (screen_x, screen_y), radius)

        # Draw selected crew highlight and path
        if selected_crew:
            screen_x, screen_y = camera.world_to_screen(
                selected_crew.x * TILE_SIZE + TILE_SIZE // 2,
                selected_crew.y * TILE_SIZE + TILE_SIZE // 2
            )
            radius = TILE_SIZE // 2
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), radius, 2)

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