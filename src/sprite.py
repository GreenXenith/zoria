import pygame
from . import assets
from .vector import *

global registered_sprites
registered_sprites = {}

def register_sprite(name, definition):
    registered_sprites[name] = definition

class Sprite:
    texture = "none.png"
    rect = pygame.Rect(0, 0, 0, 0)

    def __init__(self, name, pos, z):
        self.name = name
        self.pos = pos
        self.z = z
        self.vel = Vector(0, 0)
        for key in registered_sprites[name]:
            value = registered_sprites[name][key]
            if not callable(value):
                setattr(self, key, value)

    def set_pos(self, vec_or_x, y = None):
        self.pos = vec_or_num(vec_or_x, y)

    def set_texture(self, filename):
        self.texture = assets.get(filename)

    def set_rect(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
    
    def get_rect(self):
        return self.rect

    def on_step(self, dtime, map, player):
        oldx = self.pos.x
        self.set_pos(self.pos.x + self.vel.x * dtime, self.pos.y)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(oldx, self.pos.y)

        oldy = self.pos.y
        self.set_pos(self.pos.x, self.pos.y + self.vel.y * dtime)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(self.pos.x, oldy)

        if "on_step" in registered_sprites[self.name]:
            registered_sprites[self.name]["on_step"](self, dtime, map, player)

