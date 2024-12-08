import pygame
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    ship = create_basic_ship()

    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game logic
        ship.update(dt)

        # Rendering
        screen.fill((0,0,0))
        draw_ship(screen, ship)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
