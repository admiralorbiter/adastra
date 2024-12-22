from world.deck import Deck
from world.room import Room
from world.ship import Ship
from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
from models.crew import CrewMember, Skill

def create_basic_ship(cable_system=None):
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
    ship.cable_system = cable_system

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