from world.deck import Deck
from world.room import Room
from world.ship import Ship
from world.modules import LifeSupportModule, ReactorModule
from world.objects import Bed, StorageContainer
from models.crew import CrewMember, Skill
from models.enemies import RangedEnemy
from world.items import FoodItem
from world.weapons import LaserTurret

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
    # Add initial food supply (50 food rations)
    storage.add_item(FoodItem(quantity=50))
    main_deck.tiles[5][4].object = storage

    # Add a laser turret for defense
    print("\n--- Adding Laser Turret ---")
    turret = LaserTurret()
    main_deck.tiles[6][7].object = turret
    turret.tile = main_deck.tiles[6][7]
    turret.x = 6
    turret.y = 7
    print(f"Turret placed at ({turret.x}, {turret.y})")

    # Create room from all non-wall tiles
    room_tiles = [tile for row in main_deck.tiles for tile in row if not tile.wall]
    room = Room(room_tiles)
    main_deck.rooms.append(room)

    ship = Ship(name="Player Ship")
    ship.add_deck(main_deck)
    ship.cable_system = cable_system
    ship.calculate_oxygen_capacity()

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

    # Add enemy in bottom right corner
    enemy = RangedEnemy("Enemy Scout")
    enemy.x = 8.0  # Make sure these are floats
    enemy.y = 8.0
    enemy.health = 100
    enemy.max_health = 100
    print(f"Enemy initialized at ({enemy.x}, {enemy.y}) with health {enemy.health}")
    ship.add_enemy(enemy)

    return ship