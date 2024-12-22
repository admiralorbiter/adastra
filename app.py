import pygame
from game.game_state import GameState
from game.event_handler import EventHandler
from rendering.ship_renderer import ShipRenderer
from rendering.cable_renderer import CableRenderer
from rendering.asset_loader import AssetLoader

def main():
    pygame.init()
    game_state = GameState()
    game_state.initialize(1280, 720)
    
    # Initialize asset loader
    AssetLoader.get_instance()
    
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

        # Update ship
        game_state.ship.update(dt)

        # Get current build item to check if cable tool is selected
        current_item = game_state.build_ui.build_system.get_current_item()
        show_cables = current_item and current_item.name == "Power Cable"

        # Rendering
        game_state.screen.fill((0, 0, 0))
        
        # Draw ship
        ship_renderer.draw_ship(
            game_state.screen, 
            game_state.ship, 
            game_state.camera, 
            None if show_cables else game_state.selected_crew,
            game_state.build_ui
        )
        
        # Draw cables if tool is selected
        if show_cables:
            cable_renderer.draw_cables(
                game_state.screen, 
                game_state.ship, 
                game_state.camera, 
                game_state.cable_system
            )
        
        # Draw UI on top
        game_state.build_ui.draw(game_state.screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
