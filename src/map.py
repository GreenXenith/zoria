import pygame
import json, math
from . import assets, dungeon, loot, tiles
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
        self.placer = loot.Placer()
        self.placer.populate(self)

    def collides(self, pos, rect):
        # Player position handling really needs to be reworked ...
        METER = self.METER
        cx = pos.x + (rect[0] / METER)
        cy = pos.y + (rect[1] / METER)
        px = int(math.floor(cx))
        py = int(math.floor(cy))
        cw = cx + (rect[2] / METER)
        ch = cy + (rect[3] / METER)
        for y in range(py - 1, py + 1 + math.ceil(rect[3] / METER)):
            for x in range(px - 1, px + 2):
                if y >= 0 and y < len(self.map[1]) and x >= 0 and x < len(self.map[1][y]):
                    tile = self.map[1][y][x]
                    if tile and tile.is_solid():
                        if cw >= x and cx <= (x + 1) and ch >= y and cy <= (y + 1):
                            return True
        return False

    def set_tile(self, x, y, z, name):
        for _ in range(len(self.map), z + 1):
            self.map.append([])

        for _ in range(len(self.map[z]), y + 1):
            self.map[z].append([])

        for _ in range(len(self.map[z][y]), x + 1):
            self.map[z][y].append(None)

        if not name:
            self.map[z][y][x] = None
        elif tiles.registered_tiles[name]:
            self.map[z][y][x] = Tile(name, (x, y, z))

    def get_tile(self, x, y, z):
        try:
            return self.map[z][y][x]
        except:
            return None
