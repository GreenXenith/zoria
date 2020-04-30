from .rand import rand
import math

def populate(map, generator, z):
    # Place stairways
    if z != 0:
        mroom = generator.rooms[int(math.ceil(len(generator.rooms) / 2))] # Middle room
        enterx = mroom.x + rand(2, mroom.width - 2)
        entery = mroom.y + rand(2, mroom.height - 3)
        map.set_tile(enterx, entery, z + 1, "map:stair_up")
        generator.enterance = (enterx, entery)

    lroom = generator.rooms[0]#len(generator.rooms) - 1] # Last room
    exitx = lroom.x + rand(2, lroom.width - 2)
    exity = lroom.y + rand(2, lroom.height - 3)
    map.set_tile(exitx, exity, z + 1, "map:stair_down")
    generator.exit = (exitx, exity)

    # Place loot
    loot = [
        ["loot:coins", 10],
        ["loot:pile", 50],
    ]

    for room in generator.rooms:
        if rand(0, 2) != 0: # 1 in 3 chance of no loot
            for y in range(1, room.height - 2):
                for x in range(1, room.width - 1):
                    if map.get_tile(x, y, z) == None:
                        placed = False
                        for l in loot:
                            if not placed and rand(1, l[1]) == 1: # 1 in n chance of placing
                                map.set_tile(room.x + x, room.y + y, z + 1, l[0])
                                placed = True


