import pygame
from .base_handler import BaseEventHandler
from world.objects import Bed
from world.pathfinding import find_path

class CrewEventHandler(BaseEventHandler):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_crew_click(event)

    def handle_crew_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = self.game_state.camera.screen_to_grid(mouse_x, mouse_y)
        
        # Check for crew selection
        for crew in self.game_state.ship.crew:
            if int(crew.x) == grid_x and int(crew.y) == grid_y:
                self.game_state.selected_crew = crew
                return True
        
        # Handle crew movement or bed interaction
        if self.game_state.selected_crew:
            deck = self.game_state.ship.decks[0]
            if grid_x < deck.width and grid_y < deck.height:
                tile = deck.tiles[grid_y][grid_x]
                self.handle_crew_destination(tile, grid_x, grid_y)

    def handle_crew_destination(self, tile, grid_x, grid_y):
        crew = self.game_state.selected_crew
        start = (int(crew.x), int(crew.y))
        goal = (grid_x, grid_y)

        if tile.object and isinstance(tile.object, Bed):
            path = find_path(self.game_state.ship.decks[0], start, goal)
            if path:
                crew.target_object = tile.object
                crew.set_path(path)
        elif tile.is_walkable():
            path = find_path(self.game_state.ship.decks[0], start, goal)
            if path:
                crew.target_object = None
                crew.set_path(path) 