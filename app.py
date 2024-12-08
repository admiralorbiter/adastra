import pygame
from world.pathfinding import find_path
from world.ship import Ship
from world.deck import Deck
from world.room import Room
from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
from models.crew import CrewMember, Skill

TILE_SIZE = 32

def create_basic_ship():
    main_deck = Deck(width=10, height=10, name="Main Deck")

    # Place modules and objects
    life_support = LifeSupportModule()
    main_deck.tiles[2][2].module = life_support

    reactor = ReactorModule(power_output=10)
    main_deck.tiles[3][2].module = reactor

    bed = Bed()
    main_deck.tiles[4][4].object = bed

    storage = StorageContainer()
    main_deck.tiles[5][4].object = storage

    # Simple one-room scenario: all tiles in one room
    all_tiles = [tile for row in main_deck.tiles for tile in row]
    room = Room(all_tiles)
    main_deck.rooms.append(room)

    ship = Ship(name="Player Ship")
    ship.add_deck(main_deck)

    # Add initial crew members with positions
    engineer = CrewMember("Sarah Chen", Skill.ENGINEER)
    engineer.x, engineer.y = 1, 1  # Top-left area
    
    pilot = CrewMember("Marcus Rodriguez", Skill.PILOT)
    pilot.x, pilot.y = 1, 3  # Middle-left area
    
    scientist = CrewMember("Dr. Emma Watson", Skill.SCIENTIST)
    scientist.x, scientist.y = 1, 5  # Bottom-left area
    
    ship.add_crew_member(engineer)
    ship.add_crew_member(pilot)
    ship.add_crew_member(scientist)

    return ship

def draw_ship(screen, ship):
    # Basic rendering logic
    # For simplicity, assume just one deck:
    if not ship.decks:
        return

    deck = ship.decks[0]
    for y in range(deck.height):
        for x in range(deck.width):
            tile = deck.tiles[y][x]

            # Decide the color based on what’s on the tile
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

            # Draw the tile as a rectangle
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Optionally draw a grid line
            pygame.draw.rect(screen, (0,0,0), rect, 1)

    # Draw crew members on the grid
    for crew_member in ship.crew:
        center_x = crew_member.x * TILE_SIZE + TILE_SIZE // 2
        center_y = crew_member.y * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 3
        color = (0, 255, 0)  # Green for crew
        pygame.draw.circle(screen, color, (center_x, center_y), radius)

    # Draw oxygen level indicator in bottom right
    screen_width, screen_height = screen.get_size()
    
    # Define indicator dimensions and position
    indicator_width = 200
    indicator_height = 30
    padding = 20
    x = screen_width - indicator_width - padding
    y = screen_height - indicator_height - padding
    
    # Draw background bar
    bg_rect = pygame.Rect(x, y, indicator_width, indicator_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)
    
    # Draw oxygen level
    oxygen_width = int((indicator_width - 4) * (ship.global_oxygen / ship.oxygen_capacity))
    oxygen_rect = pygame.Rect(x + 2, y + 2, oxygen_width, indicator_height - 4)
    oxygen_color = (100, 200, 255)  # Light blue for oxygen
    pygame.draw.rect(screen, oxygen_color, oxygen_rect)
    
    # Draw border
    pygame.draw.rect(screen, (200, 200, 200), bg_rect, 2)
    
    # Draw text
    font = pygame.font.Font(None, 24)
    text = f"O₂: {int(ship.global_oxygen)}%"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(midleft=(x + 10, y + indicator_height // 2))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    ship = create_basic_ship()
    selected_crew = None  # Track selected crew member

    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // TILE_SIZE
                grid_y = mouse_y // TILE_SIZE

                # Left click for selection
                if event.button == 1:  
                    selected_crew = None
                    for crew in ship.crew:
                        if int(crew.x) == grid_x and int(crew.y) == grid_y:
                            selected_crew = crew
                            break

                # Right click for movement (if crew selected)
                elif event.button == 3 and selected_crew:  
                    if (grid_x < ship.decks[0].width and 
                        grid_y < ship.decks[0].height and 
                        ship.decks[0].tiles[grid_y][grid_x].is_walkable()):
                        start = (int(selected_crew.x), int(selected_crew.y))
                        goal = (grid_x, grid_y)
                        path = find_path(ship.decks[0], start, goal)
                        if path:
                            selected_crew.set_path(path)

        # Update game logic
        for crew in ship.crew:
            crew.update(dt)
        ship.update(dt)

        # Rendering
        screen.fill((0,0,0))
        draw_ship(screen, ship)
        
        # Draw selected crew highlight
        if selected_crew:
            center_x = int(selected_crew.x * TILE_SIZE + TILE_SIZE // 2)
            center_y = int(selected_crew.y * TILE_SIZE + TILE_SIZE // 2)
            radius = TILE_SIZE // 2
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)

            # Optionally draw the path
            if selected_crew.move_path:
                path_points = [(int(selected_crew.x * TILE_SIZE + TILE_SIZE // 2), 
                              int(selected_crew.y * TILE_SIZE + TILE_SIZE // 2))]
                for x, y in selected_crew.move_path:
                    path_points.append((int(x * TILE_SIZE + TILE_SIZE // 2), 
                                     int(y * TILE_SIZE + TILE_SIZE // 2)))
                pygame.draw.lines(screen, (255, 255, 0), False, path_points, 2)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
