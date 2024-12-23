import pygame
import os
from utils.constants import GameConstants

class AssetLoader:
    _instance = None
    _images = {}

    def __init__(self):
        if AssetLoader._instance is not None:
            raise Exception("AssetLoader is a singleton!")
        AssetLoader._instance = self
        self.load_assets()

    @staticmethod
    def get_instance():
        if AssetLoader._instance is None:
            AssetLoader()
        return AssetLoader._instance

    def load_assets(self):
        # Load module images
        self._images['life_support'] = self.load_and_scale_image('images/o2.png')
        self._images['reactor'] = self.load_and_scale_image('images/reactor.png')
        self._images['engine'] = self.load_and_scale_image('images/engine.png')
        self._images['docking_door'] = self.load_and_scale_image('images/docking_door.png')
        # Add new object images - don't scale them initially
        self._images['bed'] = self.load_and_scale_image('images/bed.png', scale=False)
        self._images['container'] = self.load_and_scale_image('images/container.png', scale=False)

    def load_and_scale_image(self, path, scale=True):
        try:
            image = pygame.image.load(path)
            if scale:
                tile_size = GameConstants.get_instance().TILE_SIZE
                return pygame.transform.scale(image, (tile_size, tile_size))
            return image
        except pygame.error as e:
            print(f"Warning: Could not load image {path}: {e}")
            return None

    def get_image(self, key):
        return self._images.get(key) 