from vector import *

class ray:
    def __init__(self, origin, direction, time=0):
        self.origin = origin # point3
        self.direction = direction # point3
        self.time = time # float

    def at(self, t):
        return self.origin + self.direction * t
