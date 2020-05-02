import math
from . import vector
from .rand import rand
from .vector import Vector

def slime_logic(self, dtime, map, player):
    self.timer += dtime
    if self.timer >= 0.3: # Let's not do raycasting every frame
        if vector.distance(self.pos, player.pos) <= 6 \
                and len(map.raycast(self.pos, player.pos, self.z)) == 0:
            self.target_pos = player.pos

        if vector.distance(self.pos, self.target_pos) <= 1:
            self.target_pos = self.pos
            self.vel = Vector(0)
        else:
            self.vel = vector.direction(self.pos, self.target_pos) * 1.5

        if vector.distance(self.pos, player.pos) <= 1:
            if rand(0, 20) == 0:
                player.set_hp(player.hp - 2)
        
        if self.target_pos == self.pos:
            if rand(0, 2) == 0:
                dest = self.pos + Vector(rand(-5, 5), rand(-5, 5))
                if len(map.raycast(self.pos, dest, self.z)) == 0:
                    self.target_pos = dest

        self.timer = 0
