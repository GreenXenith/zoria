import pygame
import math
from . import controller, rand, vector
from .vector import Vector
from .hud import Hud

class Player:
    pos = Vector(0, 0)
    z = 1
    last_level_change = 0

    rect = pygame.Rect(0, 0, 0, 0)
    texture = "none.png"

    hp = 30
    xp = 0
    coins = 0

    key = False

    dir = 0
    vel = Vector(0, 0)

    speed = 3 # meters per second

    attacking = False

    def __init__(self, map):
        self.map = map # Bind to map for use later

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
        # Input handling
        self.vel = Vector(0, 0)

        if controller.is_down("left"):
            self.dir = 3
            self.vel.x -= 1

        if controller.is_down("right"):
            self.dir = 1
            self.vel.x += 1

        if controller.is_down("up"):
            self.dir = 2
            self.vel.y -= 1

        if controller.is_down("down"):
            self.dir = 0
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
            if not self.attacking:
                # Check for enemies
                if self.z < len(map.sprites):
                    for sprite in map.sprites[self.z]:
                        if sprite.name[:6] == "enemy:":
                            if vector.distance(self.pos, sprite.pos) <= 1.5:
                                # TODO: Fix player dir
                                rot = ((self.dir + 2) % 4) * 90
                                if abs(rot - vector.angle(self.pos, sprite.pos)) <= 45:
                                    sprite.hp -= 3 + (self.xp // 15)
                                    sprite.vel = (sprite.vel * -2) + self.vel
                                    if sprite.hp <= 0:
                                        setat = round(sprite.pos)
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

                # Slash visual
                dirs = [
                    (0, 1.5),
                    (1, 0.5),
                    (0, -0.5),
                    (-1, 0.5)
                ]
                at = self.pos + Vector(*dirs[self.dir])
                sprite = self.map.add_sprite(at.x, at.y, self.z, "player:slash")
                sprite.rot = ((self.dir + 2) % 4) * 90
                sprite.texture.set_animation(0, 3, 5)
            
            self.attacking = True
        else:
            self.attacking = False

    def set_hp(self, hp):
        self.hp = max(0, hp)
        self.hud.change("hp", {
            "text": self.hp
        })

    def get_hp(self):
        return self.hp
