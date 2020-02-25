import assets
import json
import pygame
from math import floor
from vector import Vector

class Map:
    map = []

    def load(self, filename):
        with open(filename) as file:
            data = json.load(file)
            for tile in data["tiles"]:
                assets.load(tile["texture"])

            self.map = data

    def collides(self, pos, rect):
        for y in range(int(floor(pos.y)) - 1, int(floor(pos.y)) + 2):
            for x in range(int(floor(pos.x)) - 1, int(floor(pos.x)) + 2):
                if not (x == pos.x and y == pos.y):
                    tile = self.map["tiles"][self.map["map"][y][x]]
                    if tile["solid"]:
                        rect2 = assets.get(tile["texture"]).get_rect()
                        if pos.x + (rect.width / 32) >= x and pos.x <= (x + rect2.width / 32) and \
                                pos.y + (rect.height / 32) >= y and pos.y <= (y + rect2.height / 32):
                            return True

        return False
