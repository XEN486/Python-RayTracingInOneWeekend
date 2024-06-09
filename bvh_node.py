from rtweekend import *

from aabb import *
from hittable import *
from hittable_list import *
from interval import *
from vector import *

class bvh_node(hittable):
    # the first parameter's type decides what params to use
    def __init__(self, obj_or_list, start=None, end=None):
        self.bounding_box = empty_a
        self.left = None
        self.right = None

        objects = obj_or_list
        if type(obj_or_list) == hittable_list:
            start = 0
            end = len(obj_or_list.objects)
            objects = obj_or_list.objects

        for object_index in range(start, end):
            self.bounding_box = aabb(self.bounding_box, objects[object_index].bounding_box)
        
        axis = self.bounding_box.longest_axis()
        
        if axis == 0:
            comparator = self.box_x_compare
        elif axis == 1:
            comparator = self.box_y_compare
        else:
            comparator = self.box_z_compare

        object_span = end - start

        if object_span == 1:
            self.left = self.right = objects[start]
        elif object_span == 2:
            self.left = objects[start]
            self.right = objects[start + 1]
        else:
            objects[start:end] = sorted(objects[start:end], key=lambda obj: self.get_sort_key(obj, axis))

            mid = start + (end - start) // 2
            self.left = bvh_node(objects, start, mid)
            self.right = bvh_node(objects, mid, end)

        #self.bounding_box = aabb(self.left.bounding_box, self.right.bounding_box)

    def hit(self, r, ray_t, rec):
        if not self.bounding_box.hit(r, ray_t):
            return False, rec

        hit_left, rec = self.left.hit(r, ray_t, rec)
        hit_right = False

        if self.right:
            right_t = interval(ray_t.min, rec.t if hit_left else ray_t.max)
            hit_right, rec = self.right.hit(r, right_t, rec)

        return hit_left or hit_right, rec

    @staticmethod
    def box_compare(a, b, axis_index):
        a_axis_interval = a.bounding_box.axis_interval(axis_index)
        b_axis_interval = b.bounding_box.axis_interval(axis_index)
        return a_axis_interval.min < b_axis_interval.min

    @staticmethod
    def box_x_compare(a, b):
        return bvh_node.box_compare(a,b,0)

    @staticmethod
    def box_y_compare(a, b):
        return bvh_node.box_compare(a,b,1)

    @staticmethod
    def box_z_compare(a, b):
        return bvh_node.box_compare(a,b,2)

    @staticmethod
    def get_sort_key(obj, axis_index):
        return obj.bounding_box.axis_interval(axis_index).min
        
