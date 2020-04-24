import random
import time
import math

MSIZE = 80

def rand(*args):
    random.seed(time.clock())
    return random.randint(*args)

class Placer():
    loot = [
        ["loot_gold", 30],
        ["loot_pile", 5]
    ]

    def populate(self, map):
        map["tiles"].append()
