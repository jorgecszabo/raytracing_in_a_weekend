import numpy as np
from sphere import DoesNotHitSpere, hit_sphere
from hittable import HitRecord
from interval import Interval

class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction


"""

def ray_color(ray, world):
    hit_record = HitRecord()
    hit_anything, hit_record = world.hit(ray, Interval(0, np.inf), hit_record)
    if hit_anything:
        return 0.5 * (hit_record.normal + np.array([1.0, 1.0, 1.0]))
    else:
        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])
"""
