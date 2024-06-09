from hittable import *
from interval import *
from sphere import *
from aabb import *

class hittable_list(hittable):
    def __init__(self, object=None):
        self.objects = []
        if object != None:
            self.add(object)

        self.bounding_box = aabb()

    def clear(self):
        self.objects = []

    def add(self, object):
        self.objects.append(object)     
        self.bounding_box = aabb(self.bounding_box, object.bounding_box)

    # goofy hack
    def bounding_box(self):
        return self.bounding_box

    def hit(self, r, ray_t, rec):
        temp_rec = hit_record(0, vec3(0,0,0), 0, 0)
        hit_anything = False
        closest_so_far = ray_t.max

        for object in self.objects:
            obj_hit, temp_rec = object.hit(r, interval(ray_t.min, closest_so_far), temp_rec)
            if obj_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return hit_anything, rec
