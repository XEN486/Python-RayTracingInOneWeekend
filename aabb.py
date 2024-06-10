from interval import *
from vector import *

class aabb:
    def __init__(self, min_corner=None, max_corner=None, third=None):
        if isinstance(min_corner, interval):
            self.x = min_corner
            self.y = max_corner
            self.z = third if third is not None else interval(0, 0)
        elif isinstance(min_corner, point3) and isinstance(max_corner, point3):
            self.x = interval(min_corner.x, max_corner.x)
            self.y = interval(min_corner.y, max_corner.y)
            self.z = interval(min_corner.z, max_corner.z)
        elif isinstance(min_corner, aabb) and isinstance(max_corner, aabb):
            self.x = interval(min_corner.x, max_corner.x)
            self.y = interval(min_corner.y, max_corner.y)
            self.z = interval(min_corner.z, max_corner.z)
        elif third is not None:
            self.x = min_corner
            self.y = max_corner
            self.z = third
        else:
            self.x = interval(0, 0)
            self.y = interval(0, 0)
            self.z = interval(0, 0)

        self.pad_to_minimums()

    def axis_interval(self, n):
        if n == 1:
            return self.y
        if n == 2:
            return self.z
        return self.x

    def hit(self, r, ray_t):
        t_min = ray_t.min
        t_max = ray_t.max

        ray_orig = r.origin
        ray_dir = r.direction

        for axis in range(3):
            ax = self.axis_interval(axis)
            adinv = 1 / ray_dir[axis]

            t0 = (ax.min - ray_orig[axis]) * adinv
            t1 = (ax.max - ray_orig[axis]) * adinv

            if t0 < t1:
                t_min = max(t0, t_min)
                t_max = min(t1, t_max)
            else:
                t_min = max(t1, t_min)
                t_max = min(t0, t_max)

            if t_max <= t_min:
                return False

        return True

    def longest_axis(self):
        if self.x.size() > self.y.size():
            return 0 if self.x.size() > self.z.size() else 2
        else:
            return 1 if self.y.size() > self.z.size() else 2

    def pad_to_minimums(self):
        delta = 0.0001
        if self.x.size() < delta:
            self.x = self.x.expand(delta)
        if self.y.size() < delta:
            self.y = self.y.expand(delta)
        if self.z.size() < delta:
            self.z = self.z.expand(delta)

    def min(self):
        return point3(self.x.min, self.y.min, self.z.min)

    def max(self):
        return point3(self.x.max, self.y.max, self.z.max)

    def size(self):
        return point3(self.x.size(), self.y.size(), self.z.size())

    def expand(self, delta):
        return aabb(
            interval(self.x.min - delta, self.x.max + delta),
            interval(self.y.min - delta, self.y.max + delta),
            interval(self.z.min - delta, self.z.max + delta)
        )

    @staticmethod
    def surrounding_box(box0, box1):
        small = point3(
            min(box0.x.min, box1.x.min),
            min(box0.y.min, box1.y.min),
            min(box0.z.min, box1.z.min)
        )
        large = point3(
            max(box0.x.max, box1.x.max),
            max(box0.y.max, box1.y.max),
            max(box0.z.max, box1.z.max)
        )
        return aabb(small, large)

def add_a(bbox, offset):
    return aabb(add_i(bbox.x, offset.x), add_i(bbox.y, offset.y), add_i(bbox.z, offset.z))
