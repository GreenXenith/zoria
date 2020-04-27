import pygame
from . import assets

class Sprite:
    texture = None
    rect = None

    # def __init__(self, filename):
    #     self.set_texture(filename)

    def set_texture(self, filename):
        self.texture = assets.get(filename)

    def set_rect(self, rect):
        self.rect = pygame.Rect(*rect)
    
    def get_rect(self):
        return self.rect
