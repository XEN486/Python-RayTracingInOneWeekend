from rtweekend import *
from aabb import *
from hittable import *
from hittable_list import *
from interval import *
from vector import *
import random

class bvh_node(hittable):
    def __init__(self, obj_or_list, start=None, end=None):
        self.left = None
        self.right = None

        if isinstance(obj_or_list, hittable_list):
            objects = obj_or_list.objects
            start = 0
            end = len(objects)
        else:
            objects = obj_or_list

        if start is None or end is None:
            raise ValueError("Start and end indices must be provided.")

        # Sort objects along a random axis
        axis = random.randint(0, 2)
        objects[start:end] = sorted(objects[start:end], key=lambda obj: obj.bounding_box.min()[axis])

        mid = start + (end - start) // 2
        self.left = objects[start:mid]
        self.right = objects[mid:end]

        if len(self.left) == 1:
            self.left = self.left[0]
        else:
            self.left = bvh_node(self.left, 0, len(self.left))

        if len(self.right) == 1:
            self.right = self.right[0]
        else:
            self.right = bvh_node(self.right, 0, len(self.right))

        box_left = self.left.bounding_box
        box_right = self.right.bounding_box

        if box_left is None or box_right is None:
            raise ValueError("No bounding box in bvh_node constructor.")

        self.bounding_box = self.surrounding_box(box_left, box_right)

    def hit(self, r, ray_t, rec):
        if not self.bounding_box.hit(r, ray_t):
            return False, rec

        hit_left, rec_left = self.left.hit(r, ray_t, rec)
        hit_right, rec_right = self.right.hit(r, ray_t, rec)

        if hit_left and hit_right:
            if rec_left.t < rec_right.t:
                return True, rec_left
            else:
                return True, rec_right
        elif hit_left:
            return True, rec_left
        elif hit_right:
            return True, rec_right
        else:
            return False, rec

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
