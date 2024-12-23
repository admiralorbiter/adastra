from rendering.asset_loader import AssetLoader
from utils.constants import GameConstants

class BaseRenderer:
    def __init__(self):
        self.game_constants = GameConstants.get_instance()
        self.asset_loader = AssetLoader.get_instance()

    def get_screen_position(self, camera, x, y):
        """Convert world coordinates to screen coordinates"""
        return camera.world_to_screen(
            x * self.game_constants.TILE_SIZE,
            y * self.game_constants.TILE_SIZE
        )

    def get_scaled_size(self, camera):
        """Get tile size scaled by camera zoom"""
        return int(self.game_constants.TILE_SIZE * camera.zoom) 