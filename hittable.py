from vector import *
from ray import *

class hit_record:
    def __init__(self, p, normal, mat, t, u=None, v=None, front_face=None):
        self.p = p
        self.normal = normal
        self.mat = mat
        self.t = t
        self.u = u
        self.v = v
        self.front_face = front_face

    def set_face_normal(self, r, outward_normal):
        self.front_face = dot(r.direction, outward_normal) < 0
        neg = vec3(0 - outward_normal[0], 0 - outward_normal[1], 0 - outward_normal[2])
        self.normal = outward_normal if self.front_face else neg
        
class hittable:
    def __init__(self): ...
    def hit(self, r, ray_t, rec): ...
