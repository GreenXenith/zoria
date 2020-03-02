import random
import time

def rand(*args):
    random.seed(time.clock())
    return random.randint(*args)

class Room():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.left = x
        self.right = x + width
        self.top = y
        self.bottom = y + height

def generate():
    rooms = []
    for _ in range(rand(4, 15)):
        while True:
            width = rand(6, 16)
            height = rand(6, 16)
            x = rand(0, 60)
            y = rand(0, 60)
            
            overlaps = False
            
            room1 = Room(x, y, width, height)
            for room2 in rooms:
                if room1.right >= room2.left and room1.left <= room1.right and \
                        room1.bottom >= room2.top and room1.top <= room2.bottom:
                    overlaps = True

            if not overlaps:
                rooms.append(room1)
                break
    
    return rooms
    


if __name__ == "__main__":
    rooms = generate()
    map = []

    for y in range(80):
        map.append([])
        for _ in range(80):
            map[y].append('.')

    for room in rooms:
        print(room.x, room.y, room.width, room.height)

    for room in rooms:
        for w in range(room.width):
            map[room.y][room.x + w] = "═"
            map[room.y + room.height - 1][room.x + w] = "═"

        for h in range(room.height):
            map[room.y + h][room.x] = "║"
            map[room.y + h][room.x + room.width - 1] = "║"
        
        for h in range(room.height - 2):
            for w in range(room.width - 2):
                map[room.y + h + 1][room.x + w + 1] = " "
        
        map[room.y][room.x] = "╔"
        map[room.y][room.x + room.width - 1] = "╗"
        map[room.y + room.height - 1][room.x] = "╚"
        map[room.y + room.height - 1][room.x + room.width - 1] = "╝"
    
    for y in map:
        print(''.join(y))
