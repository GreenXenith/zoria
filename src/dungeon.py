"""
Dungeon Generator
Based on https://www.jamesbaum.co.uk/blether/procedural-level-generation-rust/
"""

import random
import time
import math
from .tiles import Tile
from .vector import Vector

# Helper functions
def rand(*args):
    random.seed(time.clock())
    return random.randint(*args)

# Room class for generation handling
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

# Generator class in case its used multiple times
class Generator():
    rooms = [] # Stores room objects
    board = [] # Map of zeros and ones

    def __init__(self, width, height = None):
        self.width = width
        self.height = height or width

        for y in range(self.height + 1):
            self.board.append([])
            for _ in range(self.width + 1):
                self.board[y].append(0)

        self.place_rooms()
        self.place_corridors()

    def place_rooms(self):
        for _ in range(rand(10, 30)): # Amount of rooms
            width = rand(4, 10) # Room size
            height = rand(4, 10)
            x = rand(0, self.width - width) # Room position
            y = rand(0, self.height - height)

            if x + width > self.width:
                x = self.width - width

            if y + height > self.height:
                y = self.height - height

            collides = False
            room = Room(x, y, width, height)

            # Make sure room doesn't collide
            for other_room in self.rooms:
                if room.intersects(other_room):
                    collides = True
                    break

            # Add room if valid place
            if not collides:
                for row in range(room.height):
                    for col in range(room.width):
                        self.board[room.y + row][room.x + col] = 1

                self.rooms.append(room)

    # Connect rooms together
    def place_corridors(self):
        for i in range(len(self.rooms) - 1):
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

    def generate(self, map):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    # Floor
                    map.set_tile(x, y, 0, "map:cobble")

                    if self.board[y][x] == 1:
                        # Adjacent void (Corresponds with rotation map below)
                        asides = [
                            [1, 0],
                            [0, 1],
                            [-1, 0],
                            [0, -1]
                        ]

                        adj = 0 # How many adjacent
                        arot = 0 # Last adjacent key
                        for key in range(len(asides)):
                            off = asides[key]
                            if self.board[y + off[1]][x + off[0]] == 0:
                                adj += 1
                                arot = key

                        # Diagonal void (Corresponds with rotation map below)
                        dsides = [
                            [-1, 1],
                            [-1, -1],
                            [1, -1],
                            [1, 1]
                        ]

                        dia = 0 # How many diagonal
                        drot = None # Last diagonal key
                        for key in range(len(dsides)):
                            off = dsides[key]
                            if self.board[y + off[1]][x + off[0]] == 0:
                                dia += 1
                                # Only set key if opposite tile is floor
                                if self.board[y - off[1]][x - off[0]] == 1:
                                    if drot == None:
                                        drot = key
                                    else:
                                        if self.board[y][x + off[0]] == 0 and self.board[y + off[1]][x] == 0:
                                            drot = key

                        tile = ""
                        rmap = [2, 3, 0, 1] # Rotation map
                        if adj == 0 and dia == 1: # Need diagonals to prevent false positives with all-floor
                            tile = "map:wall_corner_outer"
                            rot = rmap[drot]
                        elif adj == 1:
                            tile = "map:wall"
                            rot = rmap[arot]
                        elif adj == 2:
                            tile = "map:wall_corner_inner"
                            rot = rmap[drot]

                        if tile != "":
                            map.set_tile(x, y, 1, tile)
                            map.get_tile(x, y, 1).set_rotation(rot)
