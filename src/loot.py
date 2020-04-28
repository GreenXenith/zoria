import random
import time
import math

def rand(*args):
    random.seed(time.clock())
    return random.randint(*args)

class Placer():
    loot = [
        ["loot:coins", 10],
        ["loot:pile", 50],
    ]

    def populate(self, map):
        if not map.generator:
            return

        for room in map.generator.rooms:
            if rand(0, 2) != 0: # 1 in 3 chance of no loot
                for y in range(1, room.height - 2):
                    for x in range(1, room.width - 1):
                        placed = False
                        for loot in self.loot:
                            if not placed and rand(1, loot[1]) == 1: # 1 in n chance of placing
                                map.set_tile(room.x + x, room.y + y, 1, loot[0])
                                placed = True

