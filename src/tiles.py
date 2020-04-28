import pygame

global registered_tiles
registered_tiles = {}

content_ids = []
content_id_map = {}

def register_tile(name, definition):
    registered_tiles[name] = definition
    content_id_map[name] = len(content_ids)
    content_ids.append(name)

def get_content_id(name):
    try:
        return content_id_map[name]
    except:
        return None

def get_tile_from_content_id(id):
    try:
        return registered_tiles[content_ids[id]]
    except:
        return None

class Tile:
    textures = ["none.png"]
    solid = True
    rotation = 0

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        for key in registered_tiles[name]:
            value = registered_tiles[name][key]
            if not callable(value):
                setattr(self, key, value)

    def get(self, key):
        try:
            return getattr(self, key)
        except:
            return None

    def set_rotation(self, rot):
        self.rotation = rot

    def get_rotation(self):
        return self.rotation

    def is_solid(self):
        return self.get("solid") == True
    
    def on_step(self, dtime, map, player):
        if "on_step" in registered_tiles[self.name]:
            registered_tiles[self.name]["on_step"](self, dtime, map, player)
