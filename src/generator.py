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
        # Map object
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

        # Generate walls
        bounds = []
        for y in range(self.height):
            bounds.append([])
            for x in range(self.width):
                wall = 0
                if self.board[y][x] > 0:
                    for x2 in range(x - 1, x + 2):
                        for y2 in range(y - 1, y + 2):
                            if self.board[y2][x2] == 0:
                                wall += 1
                bounds[y].append(wall)
        map["boundaries"] = bounds

        # Floor layer
        layer1 = self.board.copy()     
        map["renderLayers"].append(layer1)

        # Wall layer
        layer2 = []
        for y in range(self.height):
            layer2.append([])
            for _ in range(self.width):
                layer2[y].append(0)

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.board[y][x] == 1:
                    tile = 0
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

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if bounds[y][x] > 0 and layer2[y][x] == 0:
                    tile = 0
                    if bounds[y + 1][x] > 0 and bounds[y][x + 1] > 0:
                        if bounds[y][x] > 1:
                            tile = 6
                        else:
                            tile = 10
                    elif bounds[y + 1][x] > 0 and bounds[y][x - 1] > 0:
                        if bounds[y][x] > 1:
                            tile = 7
                        else:
                            tile = 11
                    elif bounds[y - 1][x] > 0 and bounds[y][x - 1] > 0:
                        if bounds[y][x] > 1:
                            tile = 8
                        else:
                            tile = 12
                    elif bounds[y - 1][x] > 0 and bounds[y][x + 1] > 0:
                        if bounds[y][x] > 1:
                            tile = 9
                        else:
                            tile = 13

                    layer2[y][x] = tile

        map["renderLayers"].append(layer2)

        return map
