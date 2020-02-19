import pygame
from sprite import Sprite

class Player:
    x = 0
    y = 0

    hp = 100
    mp = 50
    xp = 0

    speed = 2 # meters per second

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.sprite.set_pos(self.x, self.y)

    def get_pos(self):
        return {"x": self.x, "y": self.y}
    
    def __init__(self, texture = "character.png"):
        self.sprite = Sprite(texture)