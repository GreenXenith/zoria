import pygame
import math, time
from . import controller, map, rand, vector
from .vector import Vector
from .hud import Hud

class Player:
    def __init__(self, texture = "none.png", rect = pygame.Rect(0, 0, 0, 0)):
        self.pos = Vector(0, 0)
        self.z = 1
        self.last_level_change = 0

        self.rect = rect
        self.texture = texture

        self.hp = 15
        self.dead = False
        self.death_timer = 0

        self.xp = 0
        self.coins = 0

        self.key = False

        self.dir = 1
        self.vel = Vector(0, 0)
        self.look = Vector(1, 0)

        self.speed = 3 # meters per second

        self.attacking = False
        self.last_attack = 0

        # Add HUD info
        self.hud = Hud()

        self.hud.add("coin", [0, 0.9], {
            "type": "image",
            "texture": "hud_coin.png",
            "scale": 2
        })

        self.hud.add("coincount", [0.08, 0.92], {
            "type": "text",
            "text": 0,
            "size": 15,
        })

        self.hud.add("heart", [0, 0.8], {
            "type": "image",
            "texture": "hud_heart.png",
            "scale": 2
        })

        self.hud.add("hp", [0.08, 0.82], {
            "type": "text",
            "text": self.hp,
            "size": 15
        })

        self.hud.add("shiny", [0, 0.7], {
            "type": "image",
            "texture": "hud_xp.png",
            "scale": 2
        })

        self.hud.add("xp", [0.08, 0.72], {
            "type": "text",
            "text": self.xp,
            "size": 15
        })

    def set_pos(self, vec_or_x, y = None):
        self.pos = vector.vec_or_num(vec_or_x, y)

    def update(self, dtime, map):
        if self.dead:
            self.death_timer += dtime
            if self.death_timer >= 6:
                map.reset()
                map.generate(0)

                self.__init__(self.texture, self.rect)
                mroom = map.generators[0].rooms[int(math.ceil(len(map.generators[0].rooms) / 2))]
                self.set_pos(mroom.cx, mroom.cy)

                self.fade.text = "You died."
                self.fade.rate = -64
                self.fade.start = 255
            return

        # Input handling
        self.vel = Vector(0, 0)

        if controller.is_down("left"):
            self.dir = 2
            self.look = Vector(-1, 0)
            self.vel.x -= 1

        if controller.is_down("right"):
            self.dir = 0
            self.look = Vector(1, 0)
            self.vel.x += 1

        if controller.is_down("up"):
            self.dir = 3
            self.look = Vector(0, -1)
            self.vel.y -= 1

        if controller.is_down("down"):
            self.dir = 1
            self.look = Vector(0, 1)
            self.vel.y += 1

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel * math.sqrt(0.5)

        oldx = self.pos.x
        self.set_pos(self.pos.x + self.vel.x * self.speed * dtime, self.pos.y)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(oldx, self.pos.y)

        oldy = self.pos.y
        self.set_pos(self.pos.x, self.pos.y + self.vel.y * self.speed * dtime)

        if map.collides(self.pos, self.z, self.rect):
            self.set_pos(self.pos.x, oldy)

        # Animations
        if controller.is_down("up") or controller.is_down("down") or \
                controller.is_down("left") or controller.is_down("right"):
            self.texture.set_animation(self.dir * 4, (self.dir * 4) + 3, self.speed * 2)
        else:
            self.texture.set_animation(self.dir * 4, self.dir * 4, 0)

        # Do attacking
        if controller.is_down("attack"):
            if not self.attacking and time.time() - self.last_attack >= 0.7:
                self.last_attack = time.time()

                # Slash visual
                dirs = [
                    (1, 0.5),
                    (0, 1.5),
                    (-1, 0.5),
                    (0, -0.5),
                ]
                at = self.pos + Vector(*dirs[self.dir])
                slash = map.add_sprite(at.x, at.y, self.z, "player:slash")
                slash.rot = ((self.dir + 1) % 4) * -90
                slash.texture.set_animation(0, 3, 5)

                # Check for enemies
                # This probably shouldnt be handled by the player but whatever
                if self.z < len(map.sprites):
                    for sprite in map.sprites[self.z]:
                        if sprite.name[:6] == "enemy:":
                            if vector.distance(slash.pos, sprite.pos) <= 1:
                                sprite.hp -= 3 + (self.xp // 15)
                                sprite.vel = (sprite.vel * -2) + self.vel + (self.look * 2) # Knockback
                                if sprite.hp <= 0:
                                    setat = round(sprite.pos)
                                    # BUG: Corpses may remove keys and doorways
                                    map.set_tile(int(setat.x), int(setat.y), int(sprite.z), sprite.name + "_dead")
                                    map.remove_sprite(sprite.id)
                                    drop = rand.rand(0, 7)
                                    if drop == 0:
                                        item = map.add_sprite(sprite.pos.x, sprite.pos.y, sprite.z, "item:health")
                                        item.texture.set_animation(0, 4, 3)
                                    elif drop == 1:
                                        item = map.add_sprite(sprite.pos.x, sprite.pos.y, sprite.z, "item:xp")
                                        item.amount = rand.rand(3, 6)
                                        item.texture.set_animation(0, 4, 4)

            self.attacking = True
        else:
            self.attacking = False

    def set_hp(self, hp):
        self.hp = max(0, hp)
        self.hud.change("hp", {
            "text": self.hp
        })

        if self.hp == 0:
            self.dead = True
            self.texture.set_animation(16, 19, 8, False)
            self.fade.rate = 96
            self.fade.start = 0
            self.fade.text = "You died."

    def get_hp(self):
        return self.hp
