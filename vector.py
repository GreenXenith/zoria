def vec_or_num(x, y = None):
    if (type(x) is int or type(x) is float) == True:
        return Vector(x, y or x)

    return x

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Vector {{x: {0}, y: {1}}}".format(self.x, self.y)

    def apply(self, func):
        return Vector(func(self.x), func(self.y))

    def __add__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x * vec.x, self.y * vec.y)

    def __div__(self, b):
        vec = vec_or_num(b)
        return Vector(self.x / vec.x, self.y / vec.y)
