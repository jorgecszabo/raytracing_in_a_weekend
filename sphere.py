import numpy as np
from hittable import Hittable


class DoesNotHitSpere(Exception):
    pass

def hit_sphere(center, radius, ray):
    origin_coordinate = center - ray.origin
    a, b, c = (
        np.linalg.norm(ray.direction) ** 2,
        -2.0 * ray.direction @ origin_coordinate,
        np.linalg.norm(origin_coordinate) ** 2 - radius ** 2
    )
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        raise DoesNotHitSpere
    else:
        return (-b - np.sqrt(discriminant)) / (2.0 * a)

class Sphere(Hittable):
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius

    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        original_coordinate = self._center - ray.origin
        a = ray.direction @ ray.direction
        h = ray.direction @ original_coordinate
        c = (original_coordinate @ original_coordinate) - self._radius ** 2

        discriminant = h ** 2 - a * c
        if discriminant < 0:
            return False, hit_record

        discriminant_sqrt = np.sqrt(discriminant)
        root = (h - discriminant_sqrt) / a
        if root <= ray_tmin or ray_tmax <= root:
            root = (h + discriminant_sqrt) / a
            if root <= ray_tmin or ray_tmax <= root:
                return False, hit_record

        hit_record.t = root
        hit_record.point = ray.at(root)
        hit_record.normal = (hit_record.point - self._center) / self._radius
        outward_normal = (hit_record.point - self._center) / self._radius
        hit_record.set_face_normal(ray, outward_normal)
        return True, hit_record
