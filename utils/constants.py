class GameConstants:
    _instance = None
    
    def __init__(self):
        if GameConstants._instance is not None:
            raise Exception("GameConstants is a singleton!")
        GameConstants._instance = self
        self._tile_size = 32  # Default tile size
        
    @staticmethod
    def get_instance():
        if GameConstants._instance is None:
            GameConstants()
        return GameConstants._instance
        
    @property
    def TILE_SIZE(self):
        return self._tile_size
        
    @TILE_SIZE.setter
    def TILE_SIZE(self, value):
        self._tile_size = value