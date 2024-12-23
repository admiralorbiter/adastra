import pygame
from game.game_state import GameState
from game.event_handlers.event_handler import EventHandler
from rendering.ship_renderer import ShipRenderer
from rendering.cable_renderer import CableRenderer
from rendering.asset_loader import AssetLoader
from rendering.resource_ui import ResourceUI
from rendering.time_ui import TimeUI

def main():
    pygame.init()
    game_state = GameState()
    game_state.initialize(1280, 720)
    
    # Initialize asset loader
    AssetLoader.get_instance()
    
    event_handler = EventHandler(game_state)
    ship_renderer = ShipRenderer()
    cable_renderer = CableRenderer()
    resource_ui = ResourceUI()
    time_ui = TimeUI()

    while game_state.running:
        raw_dt = game_state.clock.tick(30) / 1000.0
         
        # Handle events first
        event_handler.handle_events()
        
        # Update time manager and get scaled dt
        game_state.time_manager.update(raw_dt)
        dt = game_state.time_manager.get_scaled_dt(raw_dt)
        
        # Only update game logic if not paused
        if dt > 0:
            # Update ship (which will update all systems including crew)
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
            game_state.build_ui,
            event_handler.rect_select_start,
            event_handler.rect_select_end
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
        resource_ui.draw_oxygen_status(game_state.screen, game_state.ship, 20, 20)
        time_ui.draw_time_controls(game_state.screen, game_state.time_manager, game_state.build_ui)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
