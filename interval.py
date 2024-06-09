from rtweekend import *

class interval:
    def __init__(self, pmin=infinity, pmax=-infinity):
        # pmin/pmax could be intervals, so we need to check for that first
        if type(pmin) == interval:
            a = pmin
            b = pmax
            self.min = a.min if a.min <= b.min else b.min
            self.max = a.max if a.max >= b.max else b.max
        else:
            self.min = pmin
            self.max = pmax

    def size(self):
        return self.max - self.min

    def contains(self, x):
        return self.min <= x and x <= self.max

    def surrounds(self, x):
        return self.min < x and x < self.max

    def clamp(self, x):
        if (x < self.min): return self.min
        if (x > self.max): return self.max
        return x

    def expand(self, delta):
        padding = delta / 2
        return interval(self.min - padding, self.max + padding)

empty_i = interval(infinity, -infinity)
universe_i = interval(-infinity, infinity)
