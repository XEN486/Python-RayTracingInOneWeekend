from rtweekend import *
from hittable import *
from hittable_list import *
from aabb import *
from ray import *
from vector import *
from interval import *

class quad(hittable):
    def __init__(self, Q, u, v, mat):
        self.Q = Q
        self.u = u
        self.v = v
        self.mat = mat

        self.n = cross(u, v)
        self.normal = unit_vector(self.n)
        self.D = dot(self.normal, self.Q)
        self.w = self.n / dot(self.n, self.n)

        self.set_bounding_box()

    def set_bounding_box(self):
        bbox_diagonal1 = aabb(self.Q, self.Q+self.u+self.v)
        bbox_diagonal2 = aabb(self.Q+self.u, self.Q+self.v)
        self.bounding_box = aabb(bbox_diagonal1, bbox_diagonal2)

    def hit(self, r, ray_t, rec):
        denom = dot(self.normal, r.direction)

        if abs(denom) < 1e-8:
            return False, rec

        t = (self.D - dot(self.normal, r.origin)) / denom
        if not ray_t.contains(t):
            return False, rec

        intersection = r.at(t)
        planar_hitpt_vector = intersection - self.Q
        alpha = dot(self.w, cross(planar_hitpt_vector, self.v))
        beta = dot(self.w, cross(self.u, planar_hitpt_vector))

        is_int, rec = self.is_interior(alpha, beta, rec)
        if not is_int:
            return False, rec

        rec.t = t
        rec.p = intersection
        rec.mat = self.mat
        rec.set_face_normal(r, self.normal)

        return True, rec
    
    def is_interior(self, a, b, rec):
        unit_interval = interval(0, 1)
        if not unit_interval.contains(a) or not unit_interval.contains(b):
            return False, rec

        rec.u = a
        rec.v = b
        return True, rec

def box(a, b, mat):
    sides = hittable_list()
    
    pmin = point3(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z))
    pmax = point3(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))

    dx = vec3(pmax.x - pmin.x, 0, 0)
    dy = vec3(0, pmax.y - pmin.y, 0)
    dz = vec3(0, 0, pmax.z - pmin.z)

    sides.add(quad(point3(pmin.x, pmin.y, pmax.z), dx, dy, mat)) # front
    sides.add(quad(point3(pmax.x, pmin.y, pmax.z),-dz, dy, mat)) # right
    sides.add(quad(point3(pmax.x, pmin.y, pmin.z),-dx, dy, mat)) # back
    sides.add(quad(point3(pmin.x, pmin.y, pmin.z), dz, dy, mat)) # left
    sides.add(quad(point3(pmin.x, pmax.y, pmax.z), dx,-dz, mat)) # top
    sides.add(quad(point3(pmin.x, pmin.y, pmin.z), dx, dz, mat)) # bottom

    return sides
