from .rand import rand

def place_loot(map, z):
    loot = [
        ["loot:coins", 10],
        ["loot:pile", 50],
    ]

    for room in map.generator.rooms:
        if rand(0, 2) != 0: # 1 in 3 chance of no loot
            for y in range(1, room.height - 2):
                for x in range(1, room.width - 1):
                    placed = False
                    for l in loot:
                        if not placed and rand(1, l[1]) == 1: # 1 in n chance of placing
                            map.set_tile(room.x + x, room.y + y, 1, l[0])
                            placed = True

