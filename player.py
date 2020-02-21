import pygame
import controller
from sprite import Sprite

class Player:
    x = 0
    y = 0

    hp = 100
    mp = 50
    xp = 0

    # TODO: Fix diagonal speed
    speed = 1.5 # meters per second
    
    def __init__(self):
        self.sprite = Sprite()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.sprite.set_pos(self.x, self.y)

    def get_pos(self):
        return {"x": self.x, "y": self.y}

    def update(self, dtime, map):
        movedist = self.speed * dtime

        if controller.is_down("up"):
            pos = self.get_pos()
            if not map.is_solid(self.sprite.rect.top - movedist, pos["x"]):
                self.set_pos(pos["x"], pos["y"] - movedist)

        if controller.is_down("down"):
            pos = self.get_pos()
            if not map.is_solid(self.sprite.rect.top + 1 + movedist, pos["x"]):
                self.set_pos(pos["x"], pos["y"] + movedist)

        if controller.is_down("left"):
            pos = self.get_pos()
            if not map.is_solid(pos["y"], self.sprite.rect.left - movedist):
                self.set_pos(pos["x"] - movedist, pos["y"])

        if controller.is_down("right"):
            pos = self.get_pos()
            if not map.is_solid(pos["y"], self.sprite.rect.left + 1 + movedist):
                self.set_pos(pos["x"] + movedist, pos["y"])
