import pygame
import json, math
from . import assets, dungeon, loot
from .tiles import Tile
from .vector import Vector

class Map:
    map = []

    def __init__(self, meter):
        self.METER = meter # Pixels per 1 meter

    # def load(self, filename):
    #     with open(filename) as file:
    #         self.map = json.load(file)

    def generate(self):
        self.generator = dungeon.Generator(80)
        self.generator.generate(self)
        # self.placer = loot.Placer()
        # self.map = self.placer.populate(self.map)

    # TODO: Dont use rect h/w, use corners x/y
    def collides(self, pos, rect):
        px = int(math.floor(pos.x))
        py = int(math.floor(pos.y))
        for y in range(py - 1, py + 2):
            for x in range(px - 1, px + 2):
                if y >= 0 and y < len(self.map[1]) and x >=0 and x < len(self.map[1][y]):
                    tile = self.map[1][y][x]
                    if tile and tile.is_solid():
                        if pos.x + (rect.width / self.METER) >= x and pos.x <= (x + 1) and \
                                pos.y + (rect.height / self.METER) >= y and pos.y <= (y + 1):
                            return True
        return False

    def set_tile(self, x, y, z, name):
        for _ in range(len(self.map), z + 1):
            self.map.append([])

        for _ in range(len(self.map[z]), y + 1):
            self.map[z].append([])

        for _ in range(len(self.map[z][y]), x + 1):
            self.map[z][y].append(None)

        if name != "":
            self.map[z][y][x] = Tile(name)

    def get_tile(self, x, y, z):
        try:
            return self.map[z][y][x]
        except:
            return None
