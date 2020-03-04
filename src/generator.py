import random
import time
import math

MSIZE = 80

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

        self.cx = math.floor(self.x + (width / 2))
        self.cy = math.floor(self.y + (height / 2))
    
    def intersects(self, other):
        return self.left <= other.right and self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top

class Generator():
    rooms = []
    board = []

    def __init__(self, width, height = None):
        self.width = width
        self.height = height or width

        for y in range(self.height):
            self.board.append([])
            for _ in range(self.width):
                self.board[y].append(0)
        
        self.place_rooms()
        self.place_corridors()

    def place_rooms(self):
        for _ in range(rand(4, 15)):
            width = rand(6, 16)
            height = rand(6, 16)
            x = rand(0, 60)
            y = rand(0, 60)
            
            if x + width > self.width:
                x = self.width - width

            if y + height > self.height:
                y = self.height - height

            collides = False
            room = Room(x, y, width, height)

            for other_room in self.rooms:
                if room.intersects(other_room):
                    collides = True
                    break

            if not collides:
                self.place_room(room)
    
    def place_room(self, room):
        for row in range(room.height):
            for col in range(room.width):
                y = room.y + row
                x = room.x + col

                self.board[y][x] = 1

        self.rooms.append(room)
    
    def place_corridors(self):
        for i in range(0, len(self.rooms) - 1):
            room1 = self.rooms[i]
            room2 = self.rooms[i + 1]

            if rand(0, 2) == 0:
                if room1.cx <= room2.cx:
                    self.horiz_corridor(room1.cx, room2.cx, room1.cy)
                else:
                    self.horiz_corridor(room2.cx, room1.cx, room1.cy)
                if room1.cy <= room2.cy:
                    self.vert_corridor(room1.cy, room2.cy, room2.cx)
                else:
                    self.vert_corridor(room2.cy, room1.cy, room2.cx)
            else:
                if room1.cy <= room2.cy:
                    self.vert_corridor(room1.cy, room2.cy, room2.cx)
                else:
                    self.vert_corridor(room2.cy, room1.cy, room2.cx)
                if room1.cx <= room2.cx:
                    self.horiz_corridor(room1.cx, room2.cx, room1.cy)
                else:
                    self.horiz_corridor(room2.cx, room1.cx, room1.cy)

    def horiz_corridor(self, x1, x2, y):
        for row in range(y - 1, y + 2):
            for col in range(x1 - 1, x2 + 2):
                self.board[row][col] = 1
    
    def vert_corridor(self, y1, y2, x):
        for row in range(y1, y2 + 2):
            for col in range(x - 1, x + 2):
                self.board[row][col] = 1
    
    def get_map(self):
        map = {
            "tiles": [
                "floor_cobble.png",
                "wall_cobble_down.png",
                "wall_cobble_right.png",
                "wall_cobble_up.png",
                "wall_cobble_left.png",
                "wall_cobble_corner_nw_inner.png",
                "wall_cobble_corner_ne_inner.png",
                "wall_cobble_corner_se_inner.png",
                "wall_cobble_corner_sw_inner.png",
                "wall_cobble_corner_nw_outer.png",
                "wall_cobble_corner_ne_outer.png",
                "wall_cobble_corner_se_outer.png",
                "wall_cobble_corner_sw_outer.png"
            ],
            "renderLayers": []
        }

        layer1 = self.board.copy()     
        map["renderLayers"].append(layer1)

        layer2 = self.board.copy()
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.board[y][x] == 1:
                    tile = 1
                    if self.board[y][x - 1] == 1 and self.board[y][x + 1] == 1:
                        if self.board[y - 1][x] == 0:
                            tile = 2
                        elif self.board[y + 1][x] == 0:
                            tile = 4

                    if self.board[y - 1][x] == 1 and self.board[y + 1][x] == 1:
                        if self.board[y][x - 1] == 0:
                            tile = 3
                        elif self.board[y][x + 1] == 0:
                            tile = 5

                    layer2[y][x] = tile

        # for y in range(1, len(layer2) - 1):
        #     for x in range(1, len(layer2[y]) - 1):
        #         if layer2[y][x] == 0:
        #             tile = 0
        #             if layer2[y - 1][x] != 0 and layer2[y][x - 1] == 0:
        #                 tile = 8
        #             elif layer2[y - 1][x] != 0 and layer2[y][x + 1] != 0:
        #                 tile = 9
        #             elif layer2[y + 1][x] != 0 and layer2[y][x - 1] != 0:
        #                 tile = 7
        #             elif layer2[y + 1][x] != 0 and layer2[y][x + 1] != 0:
        #                 tile = 6

        #             layer2[y][x] = tile

        map["renderLayers"].append(layer2)

        bounds = []
        for y in range(self.height):
            bounds.append([])
            for _ in range(self.width):
                bounds[y].append(0)
        map["boundaries"] = bounds

        return map

# Drawing
if __name__ == "__main__":
    gen = Generator(80)

    draw = []
    for y in range(gen.height):
        draw.append([])
        for _ in range(gen.width):
            draw[y].append(' ')
    
    for y in range(len(gen.board)):
        for x in range(len(gen.board[y])):
            if gen.board[y][x] == 1:
                char = '.'
                if gen.board[y - 1][x] == 0 or gen.board[y + 1][x] == 0:
                    if gen.board[y][x - 1] == 1 and gen.board[y][x + 1] == 1:
                        char = '═'
                elif gen.board[y][x - 1] == 0 or gen.board[y][x + 1] == 0:
                    if gen.board[y - 1][x] == 1 and gen.board[y + 1][x] == 1:
                        char = '║'

                draw[y][x] = char

    for y in range(len(draw)):
        for x in range(len(draw[y])):
            if draw[y][x] == '.':
                char = '.'
                if draw[y - 1][x] == '║' and draw[y][x - 1] == '═':
                    char = '╝'
                elif draw[y - 1][x] == '║' and draw[y][x + 1] == '═':
                    char = '╚'
                elif draw[y + 1][x] == '║' and draw[y][x - 1] == '═':
                    char = '╗'
                elif draw[y + 1][x] == '║' and draw[y][x + 1] == '═':
                    char = '╔'

                draw[y][x] = char

    # for room in rooms:
    #     for w in range(room.width):
    #         map[room.y][room.x + w] = "═"
    #         map[room.y + room.height - 1][room.x + w] = "═"

    #     for h in range(room.height):
    #         map[room.y + h][room.x] = "║"
    #         map[room.y + h][room.x + room.width - 1] = "║"
        
    #     for h in range(room.height - 2):
    #         for w in range(room.width - 2):
    #             map[room.y + h + 1][room.x + w + 1] = " "
        
    #     map[room.y][room.x] = "╔"
    #     map[room.y][room.x + room.width - 1] = "╗"
    #     map[room.y + room.height - 1][room.x] = "╚"
    #     map[room.y + room.height - 1][room.x + room.width - 1] = "╝"
    
    # for y in map:
    #     print(''.join(y))

    for y in draw:
        print(''.join(str(i) for i in y))
