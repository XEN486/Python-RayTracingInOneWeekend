from rtweekend import *
from vector import *
from ray import *
from aabb import *
import math

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

class rotate_y(hittable):
    def __init__(self, object, angle):
        self.object = object
        radians = math.radians(angle)
        self.sin_theta = math.sin(radians)
        self.cos_theta = math.cos(radians)
        
        bounding_box = self.object.bounding_box

        min_corner = point3(float("inf"), float("inf"), float("inf"))
        max_corner = point3(-float("inf"), -float("inf"), -float("inf"))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i * bounding_box.max().x + (1 - i) * bounding_box.min().x
                    y = j * bounding_box.max().y + (1 - j) * bounding_box.min().y
                    z = k * bounding_box.max().z + (1 - k) * bounding_box.min().z

                    newx = self.cos_theta * x + self.sin_theta * z
                    newz = -self.sin_theta * x + self.cos_theta * z

                    tester = vec3(newx, y, newz)

                    min_corner[0] = min(min_corner[0], tester[0])
                    min_corner[1] = min(min_corner[1], tester[1])
                    min_corner[2] = min(min_corner[2], tester[2])

                    max_corner[0] = max(max_corner[0], tester[0])
                    max_corner[1] = max(max_corner[1], tester[1])
                    max_corner[2] = max(max_corner[2], tester[2])

        self.bounding_box = aabb(min_corner, max_corner)

    def hit(self, r, ray_t, rec):
        origin = r.origin
        direction = r.direction

        rotated_origin = point3(
            self.cos_theta * origin.x - self.sin_theta * origin.z,
            origin.y,
            self.sin_theta * origin.x + self.cos_theta * origin.z
        )

        rotated_direction = vec3(
            self.cos_theta * direction.x - self.sin_theta * direction.z,
            direction.y,
            self.sin_theta * direction.x + self.cos_theta * direction.z
        )

        rotated_r = ray(rotated_origin, rotated_direction, r.time)

        is_hit, temp_rec = self.object.hit(rotated_r, ray_t, hit_record(point3(0, 0, 0), vec3(0, 0, 0), None, float("inf")))
        if not is_hit:
            return False, rec

        p = temp_rec.p
        normal = temp_rec.normal

        rec.p = point3(
            self.cos_theta * p.x + self.sin_theta * p.z,
            p.y,
            self.sin_theta * p.x + self.cos_theta * p.z  # Corrected this line
        )
        rec.normal = vec3(
            self.cos_theta * normal.x + self.sin_theta * normal.z,
            normal.y,
            self.sin_theta * normal.x + self.cos_theta * normal.z  # Corrected this line
        )
        rec.t = temp_rec.t
        rec.mat = temp_rec.mat
        rec.front_face = temp_rec.front_face

        return True, rec

class translate(hittable):
    def __init__(self, object, offset):
        self.object = object
        self.offset = offset
        self.bounding_box = self.object.bounding_box

    def hit(self, r, ray_t, rec):
        offset_r = ray(r.origin - self.offset, r.direction, r.time)

        is_hit, temp_rec = self.object.hit(offset_r, ray_t, hit_record(None, None, None, None))
        if not is_hit:
            return False, rec

        temp_rec.p += self.offset
        rec.p = temp_rec.p
        rec.normal = temp_rec.normal
        rec.t = temp_rec.t
        rec.mat = temp_rec.mat
        rec.front_face = temp_rec.front_face

        return True, rec
