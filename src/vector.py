# Vector class used for both positional vectors and directional vectors

import math

def vec_or_num(x, y = None):
    if (type(x) is int or type(x) is float) == True:
        return Vector(x, y or x)

    return x

class Vector:
    def __init__(self, x = 0, y = None):
        self.x = float(x)
        self.y = float(y or x)

    def __repr__(self):
        return "Vector {{x: {0}, y: {1}}}".format(self.x, self.y)

    def __eq__(self, b):
        vec = vec_or_num(b)
        return self.x == vec.x and self.y == vec.y

    def __ne__(self, b):
        vec = vec_or_num(b)
        return self.x != vec.x or self.y != vec.y

    def __add__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x * vec.x, self.y * vec.y)

    def __truediv__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x / vec.x, self.y / vec.y)

    def __round__(self):
        return Vector(round(self.x), round(self.y))

    def __floor__(self):
        return Vector(math.floor(self.x), math.floor(self.y))

    def __ceil__(self):
        return Vector(math.ceil(self.x), math.ceil(self.y))

    def flip(self):
        return Vector(self.y, self.x)

def apply(v, func):
        return Vector(func(v.x), func(v.y))

def length(v):
    return math.hypot(v.x, v.y)

def normalize(v):
    l = length(v)
    if l == 0:
        return Vector(0)
    else:
        return v / l

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def direction(pos1, pos2):
    return normalize(Vector(pos2.x - pos1.x, pos2.y - pos1.y))

def dot(a, b):
    return a.x * b.x + a.y * b.y

def angle(a, b):
    mag = (length(a) * length(b))
    if mag == 0: return 0
    return dot(a, b) / mag
