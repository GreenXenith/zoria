import pygame
import math
from . import controller
from .vector import *
from .hud import Hud

class Player:
    pos = Vector(0, 0)
    z = 1
    last_level_change = 0

    rect = pygame.Rect(0, 0, 0, 0)
    texture = "none.png"

    hp = 100
    coins = 0

    key = False

    dir = 0
    vel = Vector(0, 0)

    # TODO: Fix diagonal speed
    speed = 3 # meters per second

    def __init__(self):
        self.hud = Hud()
        self.hud.add("coin", [0, 0.9], {
            "type": "image",
            "texture": "coin.png",
            "scale": 2
        })
        self.hud.add("coincount", [0.08, 0.92], {
            "type": "text",
            "text": 0,
            "size": 15,
        })

    def set_pos(self, vec_or_x, y = None):
        self.pos = vec_or_num(vec_or_x, y)

    def update(self, dtime, map):
        self.vel = Vector(0, 0)

        if controller.is_down("left"):
            self.dir = 3
            self.vel.x -= 1

        if controller.is_down("right"):
            self.dir = 1
            self.vel.x += 1

        if controller.is_down("up"):
            self.dir = 2
            self.vel.y -= 1

        if controller.is_down("down"):
            self.dir = 0
            self.vel.y += 1

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel * math.sqrt(0.5)

        oldx = self.pos.x
        self.set_pos(self.pos.x + self.vel.x * self.speed * dtime, self.pos.y)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(oldx, self.pos.y)

        oldy = self.pos.y
        self.set_pos(self.pos.x, self.pos.y + self.vel.y * self.speed * dtime)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(self.pos.x, oldy)

        if controller.is_down("up") or controller.is_down("down") or \
                controller.is_down("left") or controller.is_down("right"):
            self.texture.set_animation(self.dir * 4, (self.dir * 4) + 3, self.speed * 2)
        else:
            self.texture.set_animation(self.dir * 4, self.dir * 4, 0)
