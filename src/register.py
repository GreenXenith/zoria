import math
import random
import time
from . import controller, tiles
from .vector import Vector

# Structure tiles
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

# Stairs
def prev_level(self, _, map, player):
    # Lazy distance check
    if math.hypot(player.pos.x - self.pos[0], player.pos.y + 1 - self.pos[1]) <= 2 \
            and player.pos.y + 0.5 > self.pos[1] and controller.is_down("shift") \
            and time.time() - player.last_level_change > 0.5: # Prevent multiple shifts
        player.z = max(1, player.z - 2)
        generator = map.generators[player.z - 1]

        player.set_pos(generator.exit[0], generator.exit[1] - 1)
        player.dir = 2
        player.last_level_change = time.time()

tiles.register_tile("map:stair_up", {
    "textures": ["stair_up.png"],
    "solid": True,
    "on_step": prev_level,
})

def next_level(self, _, map, player):
    if math.hypot(player.pos.x - self.pos[0], player.pos.y + 1 - self.pos[1]) <= 1 \
            and controller.is_down("shift") and time.time() - player.last_level_change > 0.5:
        player.z += 2
        if not player.z - 1 in map.generators:
            map.generate(player.z - 1)
        generator = map.generators[player.z - 1]

        player.set_pos(generator.enterance[0], generator.enterance[1] + 0.1)
        player.dir = 0
        player.last_level_change = time.time()

tiles.register_tile("map:stair_down", {
    "textures": ["stair_down.png"],
    "solid": False,
    "on_step": next_level,
})

# Loot
def pick_up(self, _, map, player):
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
