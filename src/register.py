import math, random, time
from . import assets, controller, sprite, spritesheet, tiles
from .vector import Vector

def is_collided(pos, map, player):
    METER = map.METER
    rect = player.rect
    cx = player.pos.x + (rect[0] / METER)
    cy = player.pos.y + (rect[1] / METER)

    cw = cx + (rect[2] / METER)
    ch = cy + (rect[3] / METER)

    if cw >= pos[0] and cx <= (pos[0] + 1) and ch >= pos[1] and cy <= (pos[1] + 1):
        return True

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
def prev_level(self, dtime, map, player):
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

def unlock_next(self, dtime, map, player):
    if math.hypot(player.pos.x - self.pos[0], player.pos.y + 1 - self.pos[1]) <= 1 \
            and player.key and controller.is_down("shift") and time.time() - player.last_level_change > 0.5:

        map.set_tile(*self.pos, "map:stair_down")
        player.hud.remove("key")
        player.key = False
        player.last_level_change = time.time()

tiles.register_tile("map:stair_down_locked", {
    "textures": ["stair_down_locked.png"],
    "solid": False,
    "on_step": unlock_next,
})

def next_level(self, _, map, player):
    if math.hypot(player.pos.x - self.pos[0], player.pos.y + 1 - self.pos[1]) <= 1 \
            and controller.is_down("shift") and time.time() - player.last_level_change > 0.5:
        player.z += 2
        if not player.z - 1 in map.generators: # Generate level if new
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

# Items
def pick_up_key(self, dtime, map, player):
    if is_collided(self.pos, map, player):
        player.key = True
        player.hud.add("key", [0, 0.6], {
            "type": "image",
            "texture": "key.png",
            "scale": 1.5
        })
        map.set_tile(*self.pos, None)

tiles.register_tile("item:key", {
    "textures": ["key.png"],
    "solid": False,
    "on_step": pick_up_key
})

# Loot
def pick_up_coin(self, dtime, map, player):
    if is_collided(self.pos, map, player):
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
    "on_step": pick_up_coin
})

tiles.register_tile("loot:pile", {
    "textures": ["loot_pile.png"],
    "solid": False,
    "min_value": 6,
    "max_value": 12,
    "on_step": pick_up_coin
})

def pick_up_health(self, dtime, map, player):
    if is_collided((self.pos.x, self.pos.y), map, player):
        player.hp += 3
        player.hud.change("hp", {
            "text": player.hp
        })
        map.remove_sprite(self.id)

sprite.register_sprite("item:health", {
    "texture": spritesheet.SpriteSheet(assets.get("health.png"), 32, 32),
    "on_step": pick_up_health
})

def pick_up_xp(self, dtime, map, player):
    if is_collided((self.pos.x, self.pos.y), map, player):
        player.xp += self.amount
        player.hud.change("xp", {
            "text": player.xp
        })
        map.remove_sprite(self.id)

sprite.register_sprite("item:xp", {
    "texture": spritesheet.SpriteSheet(assets.get("xp.png"), 32, 32),
    "on_step": pick_up_xp
})

# Enemies
def spawn_slime(self, dtime, map, player):
    map.set_tile(*self.pos, None)
    sprite = map.add_sprite(*self.pos, "enemy:slime")
    sprite.hp = 4 + (2 * sprite.z)
    sprite.set_rect(0, 0, 32, 32)
    sprite.texture.set_animation(0, 3, 4)
    sprite.target_pos = Vector(self.pos[0], self.pos[1])

tiles.register_tile("enemy:slime", {
    "textures": ["slime_spawner.png"],
    "on_step": spawn_slime
})

tiles.register_tile("enemy:slime_dead", {
    "textures": ["slime_dead.png"],
    "solid": False,
})

from .slime import slime_logic

sprite.register_sprite("enemy:slime", {
    "texture": spritesheet.SpriteSheet(assets.get("slime.png"), 32, 32),
    "timer": 0,
    "target_pos": Vector(0),
    "on_step": slime_logic
})

# Effects
def slash(self, dtime, map, player):
    self.timer += dtime
    if self.timer >= 2 / 4:
        map.remove_sprite(self.id)

sprite.register_sprite("player:slash", {
    "texture": spritesheet.SpriteSheet(assets.get("magic_slash.png"), 32, 32),
    "timer": 0,
    "on_step": slash
})
