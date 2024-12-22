import pygame
from models.build import BuildUI
from world.pathfinding import find_path
from world.ship import Ship
from world.deck import Deck
from world.room import Room
from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
from models.crew import CrewMember, Skill
from world.camera import Camera

TILE_SIZE = 32

def create_basic_ship():
    main_deck = Deck(width=10, height=10, name="Main Deck")
    
    # Initialize all tiles as floors by default
    for y in range(main_deck.height):
        for x in range(main_deck.width):
            main_deck.tiles[y][x].wall = False
    
    # Add walls around the edges
    for x in range(main_deck.width):
        main_deck.tiles[0][x].wall = True  # Top wall
        main_deck.tiles[main_deck.height-1][x].wall = True  # Bottom wall
    for y in range(main_deck.height):
        main_deck.tiles[y][0].wall = True  # Left wall
        main_deck.tiles[y][main_deck.width-1].wall = True  # Right wall

    # Place modules and objects
    life_support = LifeSupportModule()
    main_deck.tiles[2][2].module = life_support

    reactor = ReactorModule(power_output=10)
    main_deck.tiles[3][2].module = reactor

    bed = Bed()
    main_deck.tiles[4][4].object = bed

    storage = StorageContainer()
    main_deck.tiles[5][4].object = storage

    # Create room from all non-wall tiles
    room_tiles = [tile for row in main_deck.tiles for tile in row if not tile.wall]
    room = Room(room_tiles)
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

def draw_ship(screen, ship, camera, selected_crew=None):
    if not ship.decks:
        return

    deck = ship.decks[0]
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

            # Use camera to convert world position to screen position
            screen_x, screen_y = camera.world_to_screen(x * TILE_SIZE, y * TILE_SIZE)
            rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Optionally draw a grid line
            pygame.draw.rect(screen, (0,0,0), rect, 1)

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    ship = create_basic_ship()
    selected_crew = None
    build_ui = BuildUI(screen.get_width())

    # Initialize camera
    camera = Camera(screen.get_width(), screen.get_height())
    # Center camera on ship
    ship_width = ship.decks[0].width * TILE_SIZE
    ship_height = ship.decks[0].height * TILE_SIZE
    camera.center_on(ship_width, ship_height)

    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Handle UI clicks first
                if build_ui.handle_click((mouse_x, mouse_y)):
                    continue

                if event.button == 3:  # Right mouse button
                    if not selected_crew:  # Only start panning if no crew selected
                        camera.start_pan(mouse_x, mouse_y)
                elif event.button == 1:  # Left mouse button
                    # Convert screen coordinates to world coordinates
                    world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
                    grid_x, grid_y = world_x // TILE_SIZE, world_y // TILE_SIZE
                    
                    # Handle selection
                    selected_crew = None
                    for crew in ship.crew:
                        if int(crew.x) == grid_x and int(crew.y) == grid_y:
                            selected_crew = crew
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Right mouse button
                    camera.stop_pan()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                camera.update_pan(mouse_x, mouse_y)

            # Handle right-click movement for selected crew
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selected_crew:
                world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
                grid_x, grid_y = world_x // TILE_SIZE, world_y // TILE_SIZE
                
                if (grid_x < ship.decks[0].width and 
                    grid_y < ship.decks[0].height and 
                    ship.decks[0].tiles[grid_y][grid_x].is_walkable()):
                    start = (int(selected_crew.x), int(selected_crew.y))
                    goal = (grid_x, grid_y)
                    path = find_path(ship.decks[0], start, goal)
                    if path:
                        selected_crew.set_path(path)

        # Rendering
        screen.fill((0,0,0))
        draw_ship(screen, ship, camera, selected_crew)
        build_ui.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
