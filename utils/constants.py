from utils.config_manager import ConfigManager

class GameConstants:
    _instance = None
    
    def __init__(self):
        if GameConstants._instance is not None:
            raise Exception("GameConstants is a singleton!")
        GameConstants._instance = self
        self._config = ConfigManager.get_instance()
        
    @staticmethod
    def get_instance():
        if GameConstants._instance is None:
            GameConstants()
        return GameConstants._instance
        
    @property
    def TILE_SIZE(self):
        return self._config.get('game.tile.size', 32)