import pygame
from sprite import Sprite

class Player:
    x = 0
    y = 0

    hp = 100
    mp = 50
    xp = 0

    sprite = Sprite("character.png")

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.sprite.set_pos(self.x, self.y)