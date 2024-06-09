from hittable import *
from vector import *
from aabb import *
import math

class sphere(hittable):
    def __init__(self, center1, radius, mat, center2=None, is_moving=False): # center1 (?)
        self.center1 = center1
        self.center2 = center2
        self.is_moving = False

        if self.center2 != None:
            self.center_vec = self.center2 - self.center1
        
        self.radius = max(0, radius)
        self.mat = mat
        
        rvec = vec3(radius, radius, radius)
        box1 = aabb(center1 - rvec, center1 + rvec)
        if is_moving == True:
            box2 = aabb(center2 - rvec, center2 + rvec)
            self.bounding_box = aabb(box1, box2)
        else:
            self.bounding_box = box1

    def hit(self, r, ray_t, rec):
        self.center = self._sphere_center(r.time) if self.is_moving else self.center1
        oc = self.center - r.origin
        a = r.direction.squared_length
        h = dot(r.direction, oc)
        c = oc.squared_length - self.radius * self.radius
        discriminant = h * h - a * c

        if discriminant < 0:
            return False, rec

        sqrtd = math.sqrt(discriminant)

        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False, rec

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p - self.center) / self.radius
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.u, rec.v = self.get_sphere_uv(outward_normal, rec.u, rec.v)
        rec.mat = self.mat

        return True, rec

    def get_sphere_uv(self, p, u, v):
        theta = math.acos(-p.y)
        phi = math.atan2(-p.z, p.x) + pi

        u = phi / (2 * pi)
        v = theta / pi

        return u, v

    def _sphere_center(self, time):
        return self.center1 + (time * self.center_vec)
