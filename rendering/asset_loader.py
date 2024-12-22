import pygame
import os

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

    def load_and_scale_image(self, path):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (32, 32))  # Scale to TILE_SIZE

    def get_image(self, key):
        return self._images.get(key) 