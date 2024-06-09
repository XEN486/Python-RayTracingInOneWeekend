from rtweekend import *
from interval import *
from vector import *

class aabb:
    def __init__(self, a=None, b=None, z=None):
        if type(a) == interval:
            self.x = a
            self.y = b
            self.z = z
        elif type(a) == point3:
            self.x = interval(a[0], b[0]) if (a[0] <= b[0]) else interval(b[0], a[0])
            self.y = interval(a[1], b[1]) if (a[1] <= b[1]) else interval(b[1], a[1])
            self.z = interval(a[2], b[2]) if (a[2] <= b[2]) else interval(b[2], a[2])
        elif type(a) == aabb:
            self.x = interval(a.x, b.x)
            self.y = interval(a.y, b.y)
            self.z = interval(a.z, b.z)
        else:
            self.x = empty_i
            self.y = empty_i
            self.z = empty_i

        self.pad_to_minimums()
        
    def axis_interval(self, n):
        if n == 1: return self.y
        if n == 2: return self.z
        return self.x

    def hit(self, r, ray_t):
        ray_orig = r.origin
        ray_dir = r.direction

        for axis in range(3):
            ax = self.axis_interval(axis)
            adinv = 1 / ray_dir[axis]

            t0 = (ax.min - ray_orig[axis]) * adinv
            t1 = (ax.max - ray_orig[axis]) * adinv

            if t0 < t1:
                if t0 > ray_t.min: ray_t.min = t0
                if t1 < ray_t.max: ray_t.max = t1
            else:
                if t1 > ray_t.min: ray_t.min = t1
                if t0 < ray_t.max: ray_t.max = t0

            if ray_t.max <= ray_t.min:
                return False

        return True

    def longest_axis(self):
        if (self.x.size() > self.y.size()):
            return 0 if self.x.size() > self.z.size() else 2
        else:
            return 1 if self.y.size() > self.z.size() else 2

    def pad_to_minimums(self):
        delta = 0.0001
        if (self.x.size() < delta): self.x = self.x.expand(delta)
        if (self.y.size() < delta): self.y = self.y.expand(delta)
        if (self.z.size() < delta): self.z = self.z.expand(delta)

empty_a = aabb(empty_i, empty_i, empty_i)
universe_a = aabb(universe_i, universe_i, universe_i)
