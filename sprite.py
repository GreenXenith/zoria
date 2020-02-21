import pygame
import assets

class Sprite:
    x = 0
    y = 0

    texture = None
    rect = None

    def set_texture(self, filename):
        self.texture = assets.get(filename)

    def set_rect(self, rect):
        self.rect = pygame.Rect(*rect)
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.rect.x = self.x
        self.rect.y = self.y

    def get_pos(self):
        return {"x": self.x, "y": self.y}

    def __init__(self, filename, rect = None):
        self.set_texture(filename)
        if rect:
            self.rect = pygame.Rect(*rect)
        else:
            self.rect = pygame.Rect(*self.texture.get_rect())
