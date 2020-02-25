import pygame
import controller
from vector import *
from sprite import Sprite

METER = 32

class Player:
    pos = Vector(0, 0)

    hp = 100
    mp = 50
    xp = 0

    dir = 0
    vel = Vector(0, 0)

    # TODO: Fix diagonal speed
    speed = 1.5 # meters per second

    def __init__(self):
        self.sprite = Sprite()

    def set_pos(self, vec_or_x, y = None):
        self.pos = vec_or_num(vec_or_x, y)

    def update(self, dtime, map):
        vx = 0
        vy = 0

        if controller.is_down("left"):
            self.dir = 3
            vx -= 1

        if controller.is_down("right"):
            self.dir = 1
            vx += 1

        if controller.is_down("up"):
            self.dir = 2
            vy -= 1

        if controller.is_down("down"):
            self.dir = 0
            vy += 1

        self.vel.x = vx
        self.vel.y = vy

        oldx = self.pos.x
        self.set_pos(self.pos.x + self.vel.x * self.speed * dtime, self.pos.y)

        if map.collides(self.pos, self.sprite.rect):
            self.set_pos(oldx, self.pos.y)

        oldy = self.pos.y
        self.set_pos(self.pos.x, self.pos.y + self.vel.y * self.speed * dtime)

        if map.collides(self.pos, self.sprite.rect):
            self.set_pos(self.pos.x, oldy)

        if controller.is_down("up") or controller.is_down("down") or \
                controller.is_down("left") or controller.is_down("right"):
            self.sprite.texture.set_animation(self.dir * 4, (self.dir * 4) + 3, 0.1)
        else:
            self.sprite.texture.set_animation(self.dir * 4, self.dir * 4, 0)
