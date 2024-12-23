from rendering.tile_renderer import TileRenderer
from rendering.module_renderer import ModuleRenderer
from rendering.object_renderer import ObjectRenderer
from rendering.crew_renderer import CrewRenderer
from rendering.enemy_renderer import EnemyRenderer
from rendering.selection_renderer import SelectionRenderer

class ShipRenderer:
    def __init__(self):
        self.tile_renderer = TileRenderer()
        self.module_renderer = ModuleRenderer()
        self.object_renderer = ObjectRenderer()
        self.crew_renderer = CrewRenderer()
        self.enemy_renderer = EnemyRenderer()
        self.selection_renderer = SelectionRenderer()

    def draw_ship(self, screen, ship, camera, selected_crew=None, selected_enemy=None,
                 build_ui=None, rect_select_start=None, rect_select_end=None):
        if not ship.decks:
            return

        deck = ship.decks[0]
        current_item = build_ui.build_system.get_current_item() if build_ui else None

        # Draw in layers
        self.tile_renderer.draw_tiles(screen, deck, camera)
        self.tile_renderer.draw_build_highlights(screen, ship, camera, current_item)
        self.object_renderer.draw_objects(screen, deck, camera)
        self.module_renderer.draw_modules(screen, deck, camera)
        self.crew_renderer.draw_crew(screen, ship.crew, camera, selected_crew)
        self.enemy_renderer.draw_enemies(screen, ship.enemies, camera, selected_enemy)
        self.crew_renderer.draw_path(screen, selected_crew, camera)
        self.selection_renderer.draw_bed_highlights(screen, deck, camera, selected_crew)
        self.selection_renderer.draw_selection(screen, deck, camera, 
                                            rect_select_start, rect_select_end)