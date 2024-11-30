from abc import ABC, abstractmethod
from interval import Interval

class HitRecord:
    def __init__(self):
        self.point, self.normal, self.t, self.front_face = None, None, None, None

    def set_face_normal(self, ray, outward_normal):
        # NOTE: the parameter `outward_normal` is assumed to have unit length.
        self.front_face = ray.direction @ outward_normal < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, ray, ray_interval, hit_record):
        pass

class HittableList(Hittable):
    def __init__(self):
        self._objects = []

    def add(self, object):
        self._objects.append(object)

    def clear(self):
        self._objects.clear()

    def hit(self, ray, ray_interval, hit_record):
        temp_hit_record = HitRecord()
        hit_anything = False
        closest_so_far = ray_interval.max

        for object in self._objects:
            new_interval = Interval(ray_interval.min, closest_so_far)
            currently_hit, temp_hit_record = object.hit(ray, new_interval, temp_hit_record)
            if currently_hit:
                hit_anything = True
                closest_so_far = temp_hit_record.t
                hit_record = temp_hit_record

        return hit_anything, hit_record