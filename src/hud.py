import pygame
import math
from . import assets

# Returns a surface that can be blitted
def make_element(defn, scale):
    element = None

    if defn["type"] == "text":
        defaults = {
            "font": "Times New Roman",
            "color": (255, 255, 255),
            "size": 45,
        }
        for key in defaults:
            if not key in defn:
                defn[key] = defaults[key]
        element = pygame.font.SysFont(defn["font"], defn["size"]).render(str(defn["text"]), False, defn["color"])
    elif defn["type"] == "image":
        if "scale" in defn:
            scale *= defn["scale"]
        element = assets.get(defn["texture"])

    if element != None:
        rect = element.get_size()
        return pygame.transform.scale(element, (math.floor(rect[0] * scale), math.floor(rect[1] * scale)))

class Hud:
    elements = {}

    def add(self, name, pos, definition):
        self.elements[name] = [pos, definition]

    def change(self, name, definition):
        for key in definition:
            self.elements[name][1][key] = definition[key]

    def set_pos(self, name, pos):
        self.elements[name][0] = pos

    def remove(self, name):
        del self.elements[name]

    def render(self, surface, scale=1.0):
        for name in self.elements:
            element = self.elements[name]
            pos = [element[0][0], element[0][1]]
            for axis in range(len(pos)):
                p = pos[axis]
                if p < 1 and p > 0: # Decimal -- Use percentage
                    size = surface.get_size()
                    pos[axis] = size[axis] * pos[axis]
            surface.blit(make_element(element[1], scale), pos)
