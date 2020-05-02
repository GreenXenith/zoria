import pygame
import json, math
from . import assets, dungeon, level, rand, sprite, tiles
from .sprite import Sprite
from .tiles import Tile
from .vector import *

class Map:
    map = []
    sprites = []
    generators = {}

    def __init__(self, meter):
        self.METER = meter # Pixels per 1 meter

    def generate(self, z):
        generator = dungeon.Generator(40 + 4 * math.floor(z / 2)) # +4m^2 per level
        generator.generate(self, z)
        self.generators[z] = generator

        level.populate(self, generator, z)

    def collides(self, pos, z, rect):
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
                if y >= 0 and y < len(self.map[z]) and x >= 0 and x < len(self.map[z][y]):
                    tile = self.map[z][y][x]
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

    def add_sprite(self, x, y, z, name):
        for _ in range(len(self.sprites), z + 1):
            self.sprites.append([])

        sprite = Sprite(name, Vector(x, y), z)
        sprite.id = rand.rand(0, 65535)
        self.sprites[z].append(sprite)
        return sprite

    def remove_sprite(self, id):
        for layer in self.sprites:
            for i in range(len(layer)):
                if layer[i].id == id:
                    layer.pop(i)
                    return

    # Bresenham's line algorithm
    # Based on https://www.codeproject.com/Articles/15604/Ray-casting-in-a-2D-tile-based-environment
    def raycast(self, pos1, pos2, z):
        p1 = Vector(pos1.x, pos1.y)
        p2 = Vector(pos2.x, pos2.y)
        result = []

        steep = abs(p2.y - p1.y) > abs(p2.x - p1.x)
        if steep:
            p1 = p1.flip()
            p2 = p2.flip()

        if p1.x > p2.x:
            oldx = p1.x
            p1.x = p2.x
            p2.x = oldx

            oldy = p1.y
            p1.y = p2.y
            p2.y = oldy

        deltax = p2.x - p1.x
        deltay = abs(p2.y - p1.y)
        error = 0
        ystep = 0
        y = p1.y
        if p1.y < p2.y:
            ystep = 0.5
        else:
            ystep = -0.5

        x = p1.x
        while x <= p2.x:
            check = (x, y)
            if steep:
                check = (y, x)

            tile = self.get_tile(math.ceil(check[0]), math.ceil(check[1]), z)
            if tile and tile.is_solid():
                result.append(check)

            error += deltay
            if (2 * error >= deltax):
                y += ystep
                error -= deltax

            x += 0.5

        return result

    def reset(self):
        self.map = []
        self.sprites = []
        self.generators = {}
