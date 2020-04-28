import random
from . import tiles
from .vector import Vector

tiles.register_tile("map:floor", {
    "textures": ["floor.png"],
})

tiles.register_tile("map:wall", {
    "textures": [
        "wall_0.png",
        "wall_1.png",
        "wall_2.png",
        "wall_3.png",
    ],
})

tiles.register_tile("map:wall_corner_inner", {
    "textures": [
        "wall_corner_inner_0.png",
        "wall_corner_inner_1.png",
        "wall_corner_inner_2.png",
        "wall_corner_inner_3.png",
    ],
})

tiles.register_tile("map:wall_corner_outer", {
    "textures": [
        "wall_corner_outer_0.png",
        "wall_corner_outer_1.png",
        "wall_corner_outer_2.png",
        "wall_corner_outer_3.png",
    ],
})

def pick_up(self, dtime, map, player):
    METER = map.METER
    rect = player.sprite.get_rect()
    cx = player.pos.x + (rect[0] / METER)
    cy = player.pos.y + (rect[1] / METER)

    cw = cx + (rect[2] / METER)
    ch = cy + (rect[3] / METER)

    if cw >= self.pos[0] and cx <= (self.pos[0] + 1) and ch >= self.pos[1] and cy <= (self.pos[1] + 1):
        player.coins += random.randint(self.min_value, self.max_value)
        player.hud.change("coincount", {
            "text": player.coins
        })
        map.set_tile(*self.pos, None)


tiles.register_tile("loot:coins", {
    "textures": ["loot_gold.png"],
    "solid": False,
    "min_value": 2,
    "max_value": 5,
    "on_step": pick_up
})

tiles.register_tile("loot:pile", {
    "textures": ["loot_pile.png"],
    "solid": False,
    "min_value": 6,
    "max_value": 12,
    "on_step": pick_up
})
