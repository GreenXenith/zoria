import pygame
import json, math
from . import assets, generator
from .vector import Vector

class Map:
    map = []

    def __init__(self, meter):
        self.METER = meter # Pixels per 1 meter

    def load(self, filename):
        with open(filename) as file:
            self.map = json.load(file)
    
    def generate(self):
        self.map = generator.new()

    def collides(self, pos, rect):
        for y in range(int(math.floor(pos.y)) - 1, int(math.floor(pos.y)) + 2):
            for x in range(int(math.floor(pos.x)) - 1, int(math.floor(pos.x)) + 2):
                if not (x == pos.x and y == pos.y):
                    if self.map["boundaries"][y][x] == 1:
                        if pos.x + (rect.width / self.METER) >= x and pos.x <= (x + 1) and \
                                pos.y + (rect.height / self.METER) >= y and pos.y <= (y + 1):
                            return True

        return False
