import pygame
from game.game_state import GameState
from game.event_handler import EventHandler
from rendering.ship_renderer import ShipRenderer
from rendering.cable_renderer import CableRenderer

def main():
    pygame.init()
    game_state = GameState()
    game_state.initialize(1280, 720)
    
    event_handler = EventHandler(game_state)
    ship_renderer = ShipRenderer()
    cable_renderer = CableRenderer()

    while game_state.running:
        dt = game_state.clock.tick(30) / 1000.0

        # Update crew members
        for crew_member in game_state.ship.crew:
            crew_member.update(dt)

        # Handle events
        event_handler.handle_events()

        # Rendering
        if game_state.cable_view_active:
            game_state.screen.fill((0, 0, 0))
            ship_renderer.draw_ship(game_state.screen, game_state.ship, game_state.camera, None, game_state.build_ui)
            cable_renderer.draw_cables(game_state.screen, game_state.ship, game_state.camera, game_state.cable_system)
        else:
            game_state.screen.fill((0, 0, 0))
            ship_renderer.draw_ship(game_state.screen, game_state.ship, game_state.camera, game_state.selected_crew, game_state.build_ui)
        game_state.build_ui.draw(game_state.screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
