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
	
    def is_solid(self, x, y):
        try:
            return self.map["tiles"][self.map["map"][round(x)][round(y)]]["solid"]
        except:
            return False
