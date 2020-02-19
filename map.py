import pygame
import json
import assets

class Map:
    map = []

    def load(self, filename):
        with open(filename) as file:
            data = json.load(file)
            for tile in data["tiles"]:
                assets.load(tile["texture"])
            
            self.map = data